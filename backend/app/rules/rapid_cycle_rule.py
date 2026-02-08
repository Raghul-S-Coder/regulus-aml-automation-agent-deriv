from datetime import timedelta

from app.config.settings import settings
from app.models.account import Account
from app.models.transaction import Transaction
from app.rules.base_rule import BaseRule, RuleResult


class RapidCycleRule(BaseRule):
    rule_id = "RULE-03"
    rule_name = "Rapid Deposit-Withdrawal"

    def evaluate(self, transaction: Transaction, account: Account, db) -> RuleResult:
        if transaction.transaction_type != "withdrawal":
            return RuleResult(False, "medium", "", self.rule_id, self.rule_name)

        window_start = transaction.transaction_date - timedelta(hours=settings.RAPID_CYCLE_HOURS)
        recent_deposit = (
            db.query(Transaction)
            .filter(
                Transaction.account_number == transaction.account_number,
                Transaction.transaction_type == "deposit",
                Transaction.transaction_date >= window_start,
                Transaction.transaction_date <= transaction.transaction_date,
            )
            .order_by(Transaction.transaction_date.desc())
            .first()
        )

        triggered = recent_deposit is not None
        description = (
            f"Withdrawal within {settings.RAPID_CYCLE_HOURS}h of a deposit"
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
