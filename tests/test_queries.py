import sqlite3

import pytest

from ciste.db.queries import get_account, get_transactions
from tests.test_seed import build


@pytest.fixture
def db_connection():
    connection = sqlite3.connect(":memory:")
    build(connection)
    yield connection
    connection.close()


def test_get_account(db_connection):
    customer = get_account("C001", db_connection)
    assert customer is not None
    assert customer.id == "C001"
    assert customer.accounts is not None

def test_get_transactions(db_connection):
    transactions = get_transactions("C001", db_connection)
    assert transactions is not None
    assert len(transactions) > 0
