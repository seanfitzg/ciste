import sqlite3
from pathlib import Path

import pytest

from ciste.db.seed import build, dump_hash, luhn_check_digit, seed

FEES_AND_TERMS = Path(__file__).parents[1] / "docs" / "fees_and_terms.md"


@pytest.fixture(scope="module")
def conn():
    connection = sqlite3.connect(":memory:")
    build(connection)
    yield connection
    connection.close()


def one(conn, sql, *params):
    return conn.execute(sql, params).fetchone()


def test_two_runs_give_identical_databases(tmp_path):
    seed(tmp_path / "a.db")
    seed(tmp_path / "b.db")
    hashes = []
    for name in ("a.db", "b.db"):
        connection = sqlite3.connect(tmp_path / name)
        hashes.append(dump_hash(connection))
        connection.close()
    assert hashes[0] == hashes[1]


def test_seed_replaces_an_existing_database(tmp_path):
    path = tmp_path / "ciste.db"
    seed(path)
    seed(path)
    connection = sqlite3.connect(path)
    assert one(connection, "SELECT COUNT(*) FROM customers")[0] == 20
    connection.close()


def test_row_counts(conn):
    assert one(conn, "SELECT COUNT(*) FROM customers")[0] == 20
    assert one(conn, "SELECT COUNT(*) FROM customers WHERE tier = 'retail'")[0] == 12
    assert one(conn, "SELECT COUNT(*) FROM customers WHERE tier = 'premium'")[0] == 8
    assert one(conn, "SELECT COUNT(*) FROM accounts")[0] == 20
    assert 40 <= one(conn, "SELECT COUNT(*) FROM cards")[0] <= 60
    assert 450 <= one(conn, "SELECT COUNT(*) FROM transactions")[0] <= 550
    assert one(conn, "SELECT COUNT(*) FROM fee_catalogue")[0] == 6


def test_each_customer_has_two_or_three_cards(conn):
    counts = conn.execute("SELECT COUNT(*) FROM cards GROUP BY account_id").fetchall()
    assert len(counts) == 20
    assert all(2 <= n <= 3 for (n,) in counts)


def test_transactions_span_three_months(conn):
    first, last = one(conn, "SELECT MIN(posted_on), MAX(posted_on) FROM transactions")
    assert "2026-08-01" <= first < "2026-08-15"
    assert "2026-10-15" < last <= "2026-10-31"


def test_ibans_and_card_numbers_are_valid(conn):
    for (iban,) in conn.execute("SELECT iban FROM accounts"):
        assert len(iban) == 22 and iban[4:8] == "CSTE"
        rearranged = iban[4:] + iban[:4]
        assert int("".join(str(int(ch, 36)) for ch in rearranged)) % 97 == 1
    for number, last4 in conn.execute("SELECT number, last4 FROM cards"):
        assert len(number) == 16 and number.startswith("400099")
        assert luhn_check_digit(number[:-1]) == int(number[-1])
        assert number[-4:] == last4


def test_e1_duplicate_merchant_charge(conn):
    rows = conn.execute(
        "SELECT account_id, card_id, merchant, amount_cents, posted_on, entry_mode FROM transactions WHERE id IN ('T90001', 'T90002')"
    ).fetchall()
    assert len(rows) == 2 and rows[0] == rows[1]
    assert rows[0][0] == "A002" and rows[0][2:] == ("Dunnes Stores", 4250, "2026-10-14", "online")


@pytest.mark.parametrize(
    "txn_id, account_id, fee_id, amount_cents, posted_on",
    [
        ("T90003", "A001", "F-OVERDRAFT", 6500, "2026-10-09"),  # E2
        ("T90004", "A013", "F-RECALL", 17500, "2026-10-02"),  # E3
        ("T90005", "A006", "F-CARD-REPL", 1000, "2026-09-21"),  # E4
        ("T90007", "A005", "F-CARD-EXPRESS", 2500, "2026-10-18"),  # E7
        ("T90008", "A010", "F-RETURNED", 1200, "2026-09-05"),  # E9
        ("T90009", "A010", "F-RETURNED", 1200, "2026-10-05"),  # E9
        ("T90010", "A014", "F-OVERDRAFT", 6500, "2026-10-22"),  # E10
    ],
)
def test_fixed_fee_edge_cases(conn, txn_id, account_id, fee_id, amount_cents, posted_on):
    row = one(conn, "SELECT account_id, kind, fee_id, amount_cents, posted_on FROM transactions WHERE id = ?", txn_id)
    assert row == (account_id, "fee", fee_id, amount_cents, posted_on)


def test_e4_already_refunded_fee(conn):
    assert one(conn, "SELECT transaction_id, amount_cents, status FROM refunds WHERE id = 'R001'") == ("T90005", 1000, "approved")


def test_e5_frozen_card(conn):
    account_id, kind, status = one(conn, "SELECT account_id, kind, status FROM cards WHERE id = 'K005'")
    assert (account_id, kind, status) == ("A003", "debit", "frozen")
    (last,) = one(conn, "SELECT MAX(posted_on) FROM transactions WHERE card_id = 'K005'")
    assert last is not None and last < "2026-10-20"
    assert one(conn, "SELECT COUNT(*) FROM cards WHERE status = 'frozen'")[0] == 1


def test_e6_chip_and_pin_transaction(conn):
    row = one(
        conn,
        "SELECT t.account_id, t.merchant, t.amount_cents, t.entry_mode, t.posted_on, c.kind "
        "FROM transactions t JOIN cards c ON c.id = t.card_id WHERE t.id = 'T90006'",
    )
    assert row == ("A004", "Maxol Service Station", 5800, "chip_pin", "2026-10-11", "debit")


def test_e8_prior_escalation(conn):
    assert one(conn, "SELECT customer_id, reason, created_on FROM escalations WHERE id = 'E001'") == (
        "C007",
        "Customer asked for a human",
        "2026-09-30",
    )


def test_e11_open_dispute(conn):
    row = one(conn, "SELECT transaction_id, status, reason_code FROM disputes WHERE reference = 'D-0001'")
    assert row == ("T90011", "open", "not_received")
    txn = one(conn, "SELECT account_id, merchant, amount_cents, entry_mode, posted_on FROM transactions WHERE id = 'T90011'")
    assert txn == ("A015", "Booking.com", 31000, "online", "2026-09-12")


def test_second_refund_of_the_same_fee_is_impossible(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute("INSERT INTO refunds VALUES ('R999', 'T90005', 500, 'approved', '2026-10-01')")
    conn.rollback()


def test_fee_and_merchant_charge_columns_are_exclusive(conn):
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO transactions VALUES ('T99999', 'A001', NULL, 'fee', 100, 'Lidl', 'F-INTL', NULL, '2026-10-01', 'x')"
        )
    conn.rollback()


def test_no_refund_targets_a_merchant_charge(conn):
    count = one(conn, "SELECT COUNT(*) FROM refunds r JOIN transactions t ON t.id = r.transaction_id WHERE t.kind = 'merchant_charge'")
    assert count[0] == 0
    assert one(conn, "SELECT COUNT(*) FROM refunds")[0] == 1


def test_fees_match_the_catalogue_and_the_terms(conn):
    mismatched = one(
        conn,
        "SELECT COUNT(*) FROM transactions t JOIN fee_catalogue f ON f.id = t.fee_id WHERE t.amount_cents != f.amount_cents",
    )
    assert mismatched[0] == 0
    terms = FEES_AND_TERMS.read_text(encoding="utf-8")
    for (section,) in conn.execute("SELECT ft_section FROM fee_catalogue"):
        assert f"**{section}**" in terms


def test_fee_limits_per_calendar_month(conn):
    rows = conn.execute(
        "SELECT account_id, fee_id, substr(posted_on, 1, 7), COUNT(*) FROM transactions "
        "WHERE fee_id IN ('F-OVERDRAFT', 'F-RETURNED') GROUP BY 1, 2, 3"
    ).fetchall()
    for _, fee_id, _, n in rows:
        assert n <= (1 if fee_id == "F-OVERDRAFT" else 3)


def test_regular_spenders_have_no_fees(conn):
    ids = ("A008", "A009", "A012", "A017", "A018", "A019", "A020")
    marks = ",".join("?" * len(ids))
    assert one(conn, f"SELECT COUNT(*) FROM transactions WHERE kind = 'fee' AND account_id IN ({marks})", *ids)[0] == 0


def test_only_c011_goes_below_zero_once(conn):
    negative = conn.execute("SELECT id FROM accounts WHERE balance_cents < 0").fetchall()
    assert negative == [("A011",)]
    assert one(conn, "SELECT COUNT(*) FROM transactions WHERE account_id = 'A011' AND fee_id = 'F-OVERDRAFT'")[0] == 1


def test_balances_follow_from_transactions(conn):
    for account_id, balance, spent in conn.execute(
        "SELECT a.id, a.balance_cents, SUM(t.amount_cents) FROM accounts a JOIN transactions t ON t.account_id = a.id GROUP BY a.id"
    ):
        # opening balance = balance + spent; every Account but C011's stays positive overall
        assert balance + spent > 0, account_id
