import sqlite3
from pathlib import Path

from ciste.db.models import Account, Customer, Transaction

DB_PATH = Path(__file__).parents[3] / "data" / "ciste.db"


def get_connection(CISTE_DB_PATH=DB_PATH) -> sqlite3.Connection:
    return sqlite3.connect(CISTE_DB_PATH)


def get_account(conn: sqlite3.Connection, customer_id: str) -> Customer:
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


def get_transactions(
    db_connection: sqlite3.Connection,
    customer_id: str,
    start_date: str | None = None,
    end_date: str | None = None,
    merchant: str | None = None,
) -> list[Transaction]:

    sql = """SELECT t.id, t.account_id, t.amount_cents, t.posted_on
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            WHERE a.customer_id = ?"""

    params = (customer_id,)

    if start_date is not None and end_date is not None:
        sql += " AND t.posted_on BETWEEN ? AND ?"
        params += (start_date, end_date)

    if merchant is not None:
        sql += " AND t.merchant = ?"
        params += (merchant,)

    sql += " ORDER BY t.posted_on DESC LIMIT 50"

    transaction_rows = db_connection.execute(
        sql,
        params,
    ).fetchall()

    return [Transaction(*row) for row in transaction_rows]
