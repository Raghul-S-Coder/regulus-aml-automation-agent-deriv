from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.models.account import Account
from app.models.transaction import Transaction


@dataclass
class RuleResult:
    triggered: bool
    severity: str
    description: str
    rule_id: str
    rule_name: str


class BaseRule(ABC):
    rule_id: str
    rule_name: str

    @abstractmethod
    def evaluate(self, transaction: Transaction, account: Account, db) -> RuleResult:
        """Evaluate a transaction and return a RuleResult."""
        raise NotImplementedError
