from app.config.settings import settings
from app.models.account import Account
from app.models.customer import Customer
from app.models.transaction import Transaction
from app.rules.base_rule import BaseRule, RuleResult


class CrossBorderRule(BaseRule):
    rule_id = "RULE-05"
    rule_name = "Cross-Border Mismatch"

    def evaluate(self, transaction: Transaction, account: Account, db) -> RuleResult:
        if transaction.transaction_type != "deposit":
            return RuleResult(False, settings.CROSS_BORDER_ALERT_SEVERITY, "", self.rule_id, self.rule_name)

        if not transaction.deposit_source_country:
            return RuleResult(False, settings.CROSS_BORDER_ALERT_SEVERITY, "", self.rule_id, self.rule_name)

        customer = db.query(Customer).filter(Customer.customer_id == account.customer_id).first()
        if not customer:
            return RuleResult(False, settings.CROSS_BORDER_ALERT_SEVERITY, "", self.rule_id, self.rule_name)

        triggered = transaction.deposit_source_country != customer.residency_country
        description = (
            f"Deposit source country {transaction.deposit_source_country} differs from residency {customer.residency_country}"
            if triggered
            else ""
        )

        return RuleResult(
            triggered=triggered,
            severity=settings.CROSS_BORDER_ALERT_SEVERITY,
            description=description,
            rule_id=self.rule_id,
            rule_name=self.rule_name,
        )
