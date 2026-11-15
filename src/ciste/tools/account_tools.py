from dataclasses import asdict

from langchain.tools import ToolRuntime, tool

from ciste.context import Context
from ciste.db.queries import get_connection, get_transactions


@tool
def get_account(runtime: ToolRuntime[Context]):
    """get_account is a tool that retrieves account information for a given customer.
    It uses the customer_id from the context to fetch the account details from the database."""

    return resolve_customer(runtime)


@tool
def list_transactions(runtime: ToolRuntime[Context]) -> list[dict]:
    """list_transactions is a tool that retrieves a list of transactions for a given customer.
    It uses the customer_id from the context to fetch the transactions from the database."""
    
    customer_id = resolve_customer(runtime)
    # Use the customer information to fetch transactions
    connection = get_connection()
    try:
        return [
            asdict(transaction)
            for transaction in get_transactions(customer_id, connection)
        ]
    finally:
        connection.close()


def resolve_customer(runtime: ToolRuntime[Context]):
    return runtime.context.customer_id
