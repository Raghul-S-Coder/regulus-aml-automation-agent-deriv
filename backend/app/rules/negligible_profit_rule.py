from sqlalchemy import desc

from app.config.settings import settings
from app.models.account import Account
from app.models.transaction import Transaction
from app.rules.base_rule import BaseRule, RuleResult


class NegligibleProfitRule(BaseRule):
    rule_id = "RULE-02"
    rule_name = "Negligible Profit Trade"

    def evaluate(self, transaction: Transaction, account: Account, db) -> RuleResult:
        triggered = False
        description = ""

        if transaction.transaction_type != "trade-sell":
            return RuleResult(False, "high", "", self.rule_id, self.rule_name)

        prior_buy = (
            db.query(Transaction)
            .filter(
                Transaction.account_number == transaction.account_number,
                Transaction.transaction_type == "trade-buy",
                Transaction.transaction_date <= transaction.transaction_date,
            )
            .order_by(desc(Transaction.transaction_date))
            .first()
        )

        if prior_buy:
            profit = transaction.transaction_amount - prior_buy.transaction_amount
            if abs(profit) <= settings.NEGLIGIBLE_PROFIT_THRESHOLD:
                triggered = True
                description = (
                    f"Trade profit {profit} within negligible threshold {settings.NEGLIGIBLE_PROFIT_THRESHOLD}"
                )

        return RuleResult(
            triggered=triggered,
            severity="high",
            description=description,
            rule_id=self.rule_id,
            rule_name=self.rule_name,
        )
