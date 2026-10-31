"""Rebuild ciste.db from docs/seed_spec.md (CIS-0-3).

Run with `python -m ciste.db.seed [path]`. The build is deterministic: it uses
random.Random(SEED) and a fixed "today", never the system clock, so two runs give an
identical iterdump().
"""

import hashlib
import itertools
import json
import random
import sqlite3
import sys
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

SEED = 20261031
TODAY = date(2026, 10, 31)
FIRST_DAY = date(2026, 8, 1)
DAYS = (TODAY - FIRST_DAY).days + 1
SCHEMA = Path(__file__).with_name("schema.sql")

FROZEN_CARD = "K005"
FROZEN_CARD_LAST_USE = date(2026, 10, 19)
HEAVY_SPENDERS = {"C011", "C016"}
# Customers whose notes allow Fees beyond their fixed edge-case rows. C011's only Fee is the
# overdraft that marks its dip below zero; C016's are all international transfers.
RANDOM_FEE_CUSTOMERS = {"C001", "C002", "C003", "C004", "C005", "C006", "C007", "C010", "C013", "C014", "C015"}

# (id, name, amount_cents, ft_section)
FEES = [
    ("F-OVERDRAFT", "Unarranged overdraft", 6500, "FT-3.2"),
    ("F-CARD-REPL", "Card replacement", 1000, "FT-4.2"),
    ("F-CARD-EXPRESS", "Express card delivery", 2500, "FT-4.3"),
    ("F-INTL", "International transfer", 1500, "FT-5.1"),
    ("F-RECALL", "International transfer recall", 17500, "FT-5.2"),
    ("F-RETURNED", "Returned payment", 1200, "FT-6.1"),
]
FEE_BY_ID = {fee[0]: fee for fee in FEES}
RANDOM_FEE_WEIGHTS = {"F-OVERDRAFT": 1, "F-CARD-REPL": 2, "F-CARD-EXPRESS": 1, "F-INTL": 4, "F-RECALL": 1, "F-RETURNED": 3}
FEE_MONTHLY_LIMIT = {"F-OVERDRAFT": 1, "F-RETURNED": 3}  # FT-3.2, FT-6.2

# (name, tier, card kinds)
CUSTOMERS = [
    ("Aoife Brennan", "retail", ("debit", "debit")),
    ("Cian Murphy", "retail", ("debit", "debit", "virtual")),
    ("Niamh Doyle", "retail", ("debit", "debit")),
    ("Seán Kavanagh", "retail", ("debit", "debit")),
    ("Ciara Walsh", "retail", ("debit", "debit", "virtual")),
    ("Oisín Byrne", "retail", ("debit", "debit")),
    ("Gráinne Ryan", "retail", ("debit", "debit")),
    ("Darragh Nolan", "retail", ("debit", "debit")),
    ("Saoirse Quinn", "retail", ("debit", "debit", "virtual")),
    ("Eoghan Hayes", "retail", ("debit", "debit")),
    ("Róisín Gallagher", "retail", ("debit", "debit")),
    ("Fionn Daly", "retail", ("debit", "debit")),
    ("Éabha Fitzpatrick", "premium", ("debit", "debit", "credit")),
    ("Tadhg Sullivan", "premium", ("debit", "debit", "credit")),
    ("Sinéad McCarthy", "premium", ("debit", "debit", "credit")),
    ("Conor Lynch", "premium", ("debit", "debit")),
    ("Orla Brady", "premium", ("debit", "debit", "virtual")),
    ("Pádraig Moran", "premium", ("debit", "debit", "credit")),
    ("Clodagh Fahy", "premium", ("debit", "debit")),
    ("Rónán Keane", "premium", ("debit", "debit", "virtual")),
]

# category -> (merchants, min_cents, max_cents, weight)
CATEGORIES = {
    "groceries": (["Dunnes Stores", "Tesco Ireland", "Lidl", "SuperValu"], 800, 9500, 38),
    "transport": (["Leap Card", "Irish Rail", "Maxol Service Station", "Circle K"], 300, 7000, 24),
    "eating_out": (["Insomnia", "Supermac's", "Bewley's", "Boojum"], 400, 4500, 30),
    "online": (["Amazon.ie", "Zalando", "Booking.com"], 1500, 32000, 8),
}
SUBSCRIPTIONS = (["Netflix", "Spotify", "Vodafone Ireland"], 800, 6000)


@dataclass
class Card:
    id: str
    account_id: str
    number: str
    kind: str
    status: str
    expires_on: date
    last_use: date | None = None  # a frozen Card is not used after this day

    @property
    def last4(self) -> str:
        return self.number[-4:]


@dataclass
class Txn:
    account_id: str
    kind: str
    amount_cents: int
    posted_on: date
    description: str
    card_id: str | None = None
    merchant: str | None = None
    fee_id: str | None = None
    entry_mode: str | None = None
    id: str | None = None  # None until generic IDs are assigned in date order
    rank: int = 0  # on the same day and Account, Merchant charges sort before Fees
    seq: int = field(default_factory=itertools.count().__next__)


def merchant_charge(account_id, card, amount_cents, merchant, entry_mode, posted_on, *, id=None, description=None):
    return Txn(
        account_id=account_id,
        kind="merchant_charge",
        amount_cents=amount_cents,
        posted_on=posted_on,
        description=description or merchant,
        card_id=card.id,
        merchant=merchant,
        entry_mode=entry_mode,
        id=id,
    )


def fee(account_id, fee_id, posted_on, *, id=None):
    _, name, amount_cents, ft_section = FEE_BY_ID[fee_id]
    return Txn(
        account_id=account_id,
        kind="fee",
        amount_cents=amount_cents,
        posted_on=posted_on,
        description=f"{name} ({ft_section})",
        fee_id=fee_id,
        id=id,
        rank=1,
    )


def _digits(text: str) -> str:
    """Letters become 10-35, as in the IBAN mod-97 check."""
    return "".join(str(int(ch, 36)) for ch in text)


def make_iban(rng: random.Random) -> str:
    bban = "CSTE" + "".join(str(rng.randrange(10)) for _ in range(14))
    check = 98 - int(_digits(bban + "IE00")) % 97
    return f"IE{check:02d}{bban}"


def luhn_check_digit(body: str) -> int:
    total = 0
    for i, ch in enumerate(reversed(body)):
        digit = int(ch)
        if i % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return (10 - total % 10) % 10


def make_card_number(rng: random.Random) -> str:
    body = "400099" + "".join(str(rng.randrange(10)) for _ in range(9))
    return body + str(luhn_check_digit(body))


def make_email(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return ascii_name.lower().replace(" ", ".") + "@example.ie"


def random_day(rng: random.Random) -> date:
    return FIRST_DAY + timedelta(days=rng.randrange(DAYS))


def pick_card(rng: random.Random, cards: list[Card], entry_mode: str, posted_on: date) -> Card:
    usable = [
        card
        for card in cards
        if (entry_mode == "online" or card.kind != "virtual")
        and (card.last_use is None or posted_on <= card.last_use)
    ]
    return rng.choice(usable)


def fixed_transactions(cards: dict[str, list[Card]]) -> dict[str, list[Txn]]:
    """The edge-case Transactions of spec section 5, by Customer ID. Their IDs never move."""

    def first_debit(customer_id):
        return next(card for card in cards[customer_id] if card.kind == "debit")

    return {
        "C001": [fee("A001", "F-OVERDRAFT", date(2026, 10, 9), id="T90003")],
        "C002": [
            merchant_charge("A002", first_debit("C002"), 4250, "Dunnes Stores", "online", date(2026, 10, 14), id=id)
            for id in ("T90001", "T90002")
        ],
        "C004": [
            merchant_charge("A004", first_debit("C004"), 5800, "Maxol Service Station", "chip_pin", date(2026, 10, 11), id="T90006")
        ],
        "C005": [fee("A005", "F-CARD-EXPRESS", date(2026, 10, 18), id="T90007")],
        "C006": [fee("A006", "F-CARD-REPL", date(2026, 9, 21), id="T90005")],
        "C010": [
            fee("A010", "F-RETURNED", date(2026, 9, 5), id="T90008"),
            fee("A010", "F-RETURNED", date(2026, 10, 5), id="T90009"),
        ],
        "C013": [fee("A013", "F-RECALL", date(2026, 10, 2), id="T90004")],
        "C014": [fee("A014", "F-OVERDRAFT", date(2026, 10, 22), id="T90010")],
        "C015": [
            merchant_charge("A015", first_debit("C015"), 31000, "Booking.com", "online", date(2026, 9, 12), id="T90011")
        ],
    }


def generate_customer_transactions(rng, customer_id, account_id, cards, fixed) -> tuple[list[Txn], int | None]:
    """All Transactions for one Customer, and the opening balance when it is not drawn later."""
    heavy = customer_id in HEAVY_SPENDERS
    target = 34 if heavy else 24 + rng.randint(-2, 2)

    fee_counts = Counter((t.fee_id, t.posted_on.strftime("%Y-%m")) for t in fixed if t.fee_id)
    fees: list[Txn] = []
    if customer_id == "C016":
        fees = [fee(account_id, "F-INTL", random_day(rng)) for _ in range(6)]
    elif customer_id in RANDOM_FEE_CUSTOMERS:
        for _ in range(rng.randint(1, 2)):
            while True:
                fee_id = rng.choices(list(RANDOM_FEE_WEIGHTS), weights=list(RANDOM_FEE_WEIGHTS.values()))[0]
                posted_on = random_day(rng)
                key = (fee_id, posted_on.strftime("%Y-%m"))
                if fee_counts[key] < FEE_MONTHLY_LIMIT.get(fee_id, 99):
                    fee_counts[key] += 1
                    fees.append(fee(account_id, fee_id, posted_on))
                    break

    charges: list[Txn] = []
    names, low, high = SUBSCRIPTIONS
    for merchant in rng.sample(names, rng.randint(0, 2)):
        day = rng.randint(1, 28)
        amount = rng.randint(low, high)
        card = rng.choice([c for c in cards if c.last_use is None])
        for month in (8, 9, 10):
            charges.append(
                merchant_charge(account_id, card, amount, merchant, "online", date(2026, month, day), description=f"{merchant} subscription")
            )

    n_plain = target - len(fixed) - len(fees) - len(charges) - (1 if customer_id == "C011" else 0)
    for _ in range(n_plain):
        category = rng.choices(list(CATEGORIES), weights=[c[3] for c in CATEGORIES.values()])[0]
        merchants, low, high, _weight = CATEGORIES[category]
        merchant = rng.choice(merchants)
        amount = rng.randint(low, high)
        entry_mode = "online" if category == "online" else rng.choices(["contactless", "chip_pin"], weights=[55, 25])[0]
        posted_on = random_day(rng)
        charges.append(merchant_charge(account_id, pick_card(rng, cards, entry_mode, posted_on), amount, merchant, entry_mode, posted_on))

    opening_balance = None
    if customer_id == "C011":
        # Balance crosses zero once, on the fifth-last Merchant charge, and earns the overdraft Fee.
        ordered = sorted(charges, key=lambda t: (t.posted_on, t.seq))
        crossing = ordered[-5]
        overshoot = rng.randint(1, crossing.amount_cents - 1)
        opening_balance = sum(t.amount_cents for t in ordered[:-4]) - overshoot
        fees.append(fee(account_id, "F-OVERDRAFT", crossing.posted_on))

    return fixed + fees + charges, opening_balance


def build(conn: sqlite3.Connection) -> None:
    """Create the schema and fill every table from the seed spec."""
    rng = random.Random(SEED)
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    conn.execute("PRAGMA foreign_keys = ON")

    card_ids = (f"K{n:03d}" for n in itertools.count(1) if f"K{n:03d}" != FROZEN_CARD)
    used_numbers: set[str] = set()
    customers, accounts, cards = [], [], {}
    for n, (name, tier, kinds) in enumerate(CUSTOMERS, start=1):
        customer_id, account_id = f"C{n:03d}", f"A{n:03d}"
        joined_on = date(2021, 1, 1) + timedelta(days=rng.randrange(1642))
        customers.append((customer_id, name, make_email(name), tier, joined_on.isoformat()))
        accounts.append([account_id, customer_id, make_iban(rng), 0, joined_on.isoformat()])
        cards[customer_id] = []
        for i, kind in enumerate(kinds):
            number = make_card_number(rng)
            while number in used_numbers:
                number = make_card_number(rng)
            used_numbers.add(number)
            frozen = customer_id == "C003" and i == 0
            cards[customer_id].append(
                Card(
                    id=FROZEN_CARD if frozen else next(card_ids),
                    account_id=account_id,
                    number=number,
                    kind=kind,
                    status="frozen" if frozen else "active",
                    expires_on=date(rng.randint(2028, 2030), rng.randint(1, 12), 28),
                    last_use=FROZEN_CARD_LAST_USE if frozen else None,
                )
            )

    fixed = fixed_transactions(cards)
    transactions: list[Txn] = []
    opening_balances: dict[str, int] = {}
    for n, (_, tier, _) in enumerate(CUSTOMERS, start=1):
        customer_id, account_id = f"C{n:03d}", f"A{n:03d}"
        txns, opening = generate_customer_transactions(rng, customer_id, account_id, cards[customer_id], fixed.get(customer_id, []))
        if opening is None:
            spent = sum(t.amount_cents for t in txns)
            cushion = rng.randint(20_000, 400_000) if tier == "retail" else rng.randint(100_000, 1_500_000)
            opening = spent + cushion
        opening_balances[account_id] = opening
        transactions += txns

    generic = sorted((t for t in transactions if t.id is None), key=lambda t: (t.posted_on, t.account_id, t.rank, t.seq))
    for number, txn in enumerate(generic, start=1):
        txn.id = f"T{number:05d}"
    transactions.sort(key=lambda t: t.id)

    spent_by_account = Counter()
    for txn in transactions:
        spent_by_account[txn.account_id] += txn.amount_cents
    for account in accounts:
        account[3] = opening_balances[account[0]] - spent_by_account[account[0]]

    conn.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?)", customers)
    conn.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?, ?)", accounts)
    conn.executemany(
        "INSERT INTO cards VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (c.id, c.account_id, c.number, c.last4, c.kind, c.status, c.expires_on.isoformat())
            for customer_cards in cards.values()
            for c in customer_cards
        ],
    )
    conn.executemany("INSERT INTO fee_catalogue VALUES (?, ?, ?, ?)", [(f[0], f[1], f[2], f[3]) for f in FEES])
    conn.executemany(
        "INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (t.id, t.account_id, t.card_id, t.kind, t.amount_cents, t.merchant, t.fee_id, t.entry_mode, t.posted_on.isoformat(), t.description)
            for t in transactions
        ],
    )
    conn.execute("INSERT INTO refunds VALUES ('R001', 'T90005', 1000, 'approved', '2026-09-25')")
    conn.execute(
        "INSERT INTO disputes VALUES ('D-0001', 'T90011', 'open', 'not_received', ?, '2026-09-15')",
        (json.dumps({"summary": "Customer says the booking was paid for but never confirmed.", "merchant_contacted": True}, sort_keys=True),),
    )
    conn.execute("INSERT INTO escalations VALUES ('E001', 'C007', 'Customer asked for a human', '2026-09-30')")
    conn.commit()


def dump_hash(conn: sqlite3.Connection) -> str:
    """SHA-256 of the iterdump() output, to compare two databases."""
    return hashlib.sha256("\n".join(conn.iterdump()).encode("utf-8")).hexdigest()


def seed(path: str | Path = "ciste.db") -> None:
    """Delete any existing database at `path` and rebuild it."""
    path = Path(path)
    path.unlink(missing_ok=True)
    conn = sqlite3.connect(path)
    try:
        build(conn)
    finally:
        conn.close()


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "ciste.db"
    seed(path)
    conn = sqlite3.connect(path)
    try:
        for table in ("customers", "accounts", "cards", "fee_catalogue", "transactions", "refunds", "disputes", "escalations"):
            print(f"{table}: {conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]}")
        print(f"hash: {dump_hash(conn)}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
