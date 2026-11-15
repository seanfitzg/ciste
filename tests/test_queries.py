import sqlite3

import pytest

from ciste.db.queries import get_customer_account, get_transactions
from ciste.db.seed import build


@pytest.fixture
def db_connection():
    connection = sqlite3.connect(":memory:")
    build(connection)
    yield connection
    connection.close()


def test_get_customer_account(db_connection):
    customer = get_customer_account(db_connection, "C001")
    assert customer is not None
    assert customer.id == "C001"
    assert customer.accounts is not None

def test_get_transactions(db_connection):
    transactions = get_transactions(db_connection, "C001")
    assert transactions is not None
    assert len(transactions) > 0
