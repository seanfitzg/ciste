import sqlite3

import pytest

from ciste.db.queries import get_account
from tests.test_seed import build


@pytest.fixture
def db_connection():
    connection = sqlite3.connect(":memory:")
    build(connection)
    yield connection
    connection.close()


def test_get_account(db_connection):
    customer = get_account("C001", db_connection)
    print(customer)
    assert customer is not None
    assert customer.id == "C001"
    assert customer.accounts is not None
