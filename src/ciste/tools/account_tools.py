from dataclasses import asdict

from langchain.tools import ToolRuntime, tool

from ciste.context import Context
from ciste.db.queries import get_connection, get_customer_account, get_transactions


@tool
def get_account(runtime: ToolRuntime[Context]):
    """get_customer_account is a tool that retrieves account information for a given customer.
    It uses the customer_id from the context to fetch the account details from the database."""

    customer_id = resolve_customer(runtime)
    # Use the customer information to fetch transactions
    connection = get_connection()
    try:
        return [
            asdict(customer)
            for customer in get_customer_account(connection, customer_id)
        ]
    finally:
        connection.close()


@tool
def list_transactions(runtime: ToolRuntime[Context]) -> list[dict]:
    """list_transactions is a tool that retrieves a list of transactions for a given customer.
    It uses the customer_id from the context to fetch the most recent 50 transactions from the database.
    The amounts returned are in cents, and the transactions are ordered by the posted_on date in descending order."""

    customer_id = resolve_customer(runtime)
    # Use the customer information to fetch transactions
    connection = get_connection()
    try:
        return [
            asdict(transaction)
            for transaction in get_transactions(
                connection, customer_id, start_date=None, end_date=None, merchant=None
            )
        ]
    finally:
        connection.close()


def resolve_customer(runtime: ToolRuntime[Context]):
    return runtime.context.customer_id
