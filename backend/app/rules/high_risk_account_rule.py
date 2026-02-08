from app.models.account import Account
from app.models.transaction import Transaction
from app.repositories.high_risk_account_repository import HighRiskAccountRepository
from app.rules.base_rule import BaseRule, RuleResult


class HighRiskAccountRule(BaseRule):
    rule_id = "RULE-06"
    rule_name = "High Risk Account"

    def evaluate(self, transaction: Transaction, account: Account, db) -> RuleResult:
        record = HighRiskAccountRepository.get_by_account(db, transaction.account_number)
        triggered = record is not None and record.high_risk_flag == 1
        description = "Account is in high risk list" if triggered else ""
        return RuleResult(
            triggered=triggered,
            severity="high",
            description=description,
            rule_id=self.rule_id,
            rule_name=self.rule_name,
        )
