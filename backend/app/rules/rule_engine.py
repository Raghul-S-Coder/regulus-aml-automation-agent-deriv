import time

from loguru import logger
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.alert import Alert
from app.models.transaction import Transaction
from app.repositories.alert_repository import AlertRepository
from app.rules.base_rule import RuleResult
from app.rules.cross_border_rule import CrossBorderRule
from app.rules.high_deposit_rule import HighDepositRule
from app.rules.high_risk_account_rule import HighRiskAccountRule
from app.rules.negligible_profit_rule import NegligibleProfitRule
from app.rules.rapid_cycle_rule import RapidCycleRule
from app.rules.velocity_rule import VelocityRule
from app.utils.datetime_utils import utc_now
from app.utils.id_generator import generate_id


class RuleEngine:
    def __init__(self) -> None:
        self.rules = [
            HighDepositRule(),
            NegligibleProfitRule(),
            RapidCycleRule(),
            VelocityRule(),
            CrossBorderRule(),
            HighRiskAccountRule(),
        ]

    def evaluate_transaction(self, db: Session, transaction: Transaction, account: Account) -> list[Alert]:
        alerts: list[Alert] = []
        for rule in self.rules:
            rule_name = type(rule).__name__
            t_rule = time.perf_counter()
            result: RuleResult = rule.evaluate(transaction, account, db)
            elapsed = round((time.perf_counter() - t_rule) * 1000, 2)
            if result.triggered:
                logger.info(f"[TRACE] RuleEngine | {rule_name} TRIGGERED | severity={result.severity} | {elapsed}ms")
                alert = Alert(
                    alert_id=generate_id("ALERT"),
                    account_number=transaction.account_number,
                    transaction_id=transaction.transaction_id,
                    alert_type=result.rule_name,
                    severity=result.severity,
                    rule_id=result.rule_id,
                    description=result.description,
                    triggered_date=utc_now(),
                )
                alerts.append(AlertRepository.create(db, alert))
            else:
                logger.debug(f"[TRACE] RuleEngine | {rule_name} not triggered | {elapsed}ms")
        return alerts
