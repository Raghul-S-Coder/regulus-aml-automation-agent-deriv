from app.config.settings import settings
from app.models.account import Account
from app.models.transaction import Transaction
from app.rules.base_rule import BaseRule, RuleResult


class HighDepositRule(BaseRule):
    rule_id = "RULE-01"
    rule_name = "High Deposit"

    def evaluate(self, transaction: Transaction, account: Account, db) -> RuleResult:
        triggered = transaction.transaction_type == "deposit" and transaction.transaction_amount >= settings.DEPOSIT_THRESHOLD
        description = (
            f"Deposit amount {transaction.transaction_amount} exceeds threshold {settings.DEPOSIT_THRESHOLD}"
            if triggered
            else ""
        )
        return RuleResult(
            triggered=triggered,
            severity="high",
            description=description,
            rule_id=self.rule_id,
            rule_name=self.rule_name,
        )
