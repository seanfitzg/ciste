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
    accounts: list[Account] | None = None

@dataclass
class Transaction:
    id: str
    account_id: str
    amount_cents: int
    posted_on: str