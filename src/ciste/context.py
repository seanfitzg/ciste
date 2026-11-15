from pydantic.dataclasses import dataclass

from ciste.db.models import AccountTier


@dataclass
class Context:
    customer_id: str
    tier: AccountTier