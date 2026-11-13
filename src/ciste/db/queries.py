import sqlite3
from typing import Literal

from pydantic.dataclasses import dataclass

AccountTier = Literal["retail", "premium"]


@dataclass
class Account:
    id: str
    customer_id: str
    iban: str
    balance_cents: int
    opened_on: str


@dataclass
class Customer:
    id: str
    name: str
    email: str
    joined_on: str
    tier: AccountTier
    accounts: list[Account] = None


def get_account(customer_id: str, conn: sqlite3.Connection) -> Customer:
    customer_row = conn.execute(
        """SELECT c.id, c.name, c.email, c.joined_on, c.tier
        FROM customers c
        WHERE c.id = ?""",
        (customer_id,),  # parameterized query, never string formatting
    ).fetchone()

    if customer_row is None:
        return None

    account_rows = conn.execute(
        """SELECT a.id, a.customer_id, a.iban, a.balance_cents, a.opened_on
            FROM accounts a
            WHERE a.customer_id = ?""",
        (customer_id,),  # parameterized query, never string formatting
    ).fetchall()

    return (
        Customer(*customer_row, accounts=[Account(*row) for row in account_rows])
        if customer_row
        else None
    )
