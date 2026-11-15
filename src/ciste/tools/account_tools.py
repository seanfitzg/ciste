from dataclasses import asdict

from langchain.tools import ToolRuntime, tool

from ciste.context import Context
from ciste.db.queries import get_connection, get_transactions


@tool
def get_account(runtime: ToolRuntime[Context]):
    # Use the context to get the customer_id and tier
    return resolve_customer(runtime)


@tool
def list_transactions(runtime: ToolRuntime[Context]) -> list[dict]:
    # Use the context to get the customer_id and tier
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
