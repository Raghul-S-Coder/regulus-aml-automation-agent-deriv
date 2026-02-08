from datetime import timedelta

from app.config.settings import settings
from app.models.account import Account
from app.models.transaction import Transaction
from app.rules.base_rule import BaseRule, RuleResult


class VelocityRule(BaseRule):
    rule_id = "RULE-04"
    rule_name = "Transaction Velocity"

    def evaluate(self, transaction: Transaction, account: Account, db) -> RuleResult:
        window_start = transaction.transaction_date - timedelta(minutes=settings.VELOCITY_WINDOW_MINUTES)
        txn_count = (
            db.query(Transaction)
            .filter(
                Transaction.account_number == transaction.account_number,
                Transaction.transaction_date >= window_start,
                Transaction.transaction_date <= transaction.transaction_date,
            )
            .count()
        )
        triggered = txn_count >= settings.VELOCITY_TXN_COUNT
        description = (
            f"{txn_count} transactions within {settings.VELOCITY_WINDOW_MINUTES} minutes"
            if triggered
            else ""
        )
        return RuleResult(
            triggered=triggered,
            severity="medium",
            description=description,
            rule_id=self.rule_id,
            rule_name=self.rule_name,
        )
