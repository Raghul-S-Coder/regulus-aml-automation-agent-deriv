import time

from loguru import logger
from sqlalchemy.orm import Session

from app.exceptions.base_exception import NotFoundException, ValidationException
from app.exceptions.error_codes import (
    ACCOUNT_INSUFFICIENT_BALANCE,
    ACCOUNT_NOT_FOUND,
    TRANSACTION_INVALID_AMOUNT,
    TRANSACTION_INVALID_TYPE,
    TRANSACTION_NOT_FOUND,
)
from app.models.account import Account
from app.models.transaction import Transaction
from app.repositories.account_repository import AccountRepository
from app.repositories.high_risk_account_repository import HighRiskAccountRepository
from app.agents.master_agent import MasterAgent
from app.repositories.transaction_repository import TransactionRepository
from app.rules.rule_engine import RuleEngine
from app.schemas.transaction import TransactionCreate
from app.utils.datetime_utils import utc_now
from app.utils.id_generator import generate_id
from app.models.high_risk_account import HighRiskAccount


class TransactionService:
    _ALLOWED_TYPES = {"deposit", "withdrawal", "trade-buy", "trade-sell"}

    @staticmethod
    def create_transaction(db: Session, data: TransactionCreate) -> Transaction:
        t0 = time.perf_counter()
        logger.info(f"[TRACE] TransactionService | create_transaction START | account={data.account_number} type={data.transaction_type} amount={data.transaction_amount}")

        account = db.query(Account).filter(Account.account_number == data.account_number).first()
        if not account:
            raise NotFoundException(ACCOUNT_NOT_FOUND, "Account not found")
        if data.transaction_amount <= 0:
            raise ValidationException(TRANSACTION_INVALID_AMOUNT, "Transaction amount must be positive")
        if data.transaction_type not in TransactionService._ALLOWED_TYPES:
            raise ValidationException(TRANSACTION_INVALID_TYPE, "Invalid transaction type")
        if data.transaction_type in {"withdrawal", "trade-buy"} and account.balance_amount < data.transaction_amount:
            raise ValidationException(ACCOUNT_INSUFFICIENT_BALANCE, "Insufficient balance")

        transaction_date = data.transaction_date or utc_now()
        transaction = Transaction(
            transaction_id=generate_id("TXN"),
            account_number=data.account_number,
            transaction_amount=data.transaction_amount,
            transaction_currency=data.transaction_currency,
            transaction_date=transaction_date,
            transaction_type=data.transaction_type,
            purpose=data.purpose,
            deposit_source_type=data.deposit_source_type,
            deposit_source_value=data.deposit_source_value,
            deposit_source_country=data.deposit_source_country,
            transaction_status="pending",
        )
        transaction = TransactionRepository.create(db, transaction)
        logger.info(f"[TRACE] TransactionService | txn created | id={transaction.transaction_id}")

        # --- Rule evaluation ---
        t_rules = time.perf_counter()
        logger.info(f"[TRACE] TransactionService | RuleEngine evaluation START | txn={transaction.transaction_id}")
        alerts = RuleEngine().evaluate_transaction(db, transaction, account)
        elapsed_rules = round((time.perf_counter() - t_rules) * 1000, 2)
        logger.info(f"[TRACE] TransactionService | RuleEngine evaluation END | {len(alerts)} alerts triggered | {elapsed_rules}ms")

        if alerts:
            transaction.transaction_status = "held"
            TransactionRepository.update(db, transaction)
            logger.info(f"[TRACE] TransactionService | txn status -> held | alerts={[a.alert_id for a in alerts]}")

            existing_high_risk = HighRiskAccountRepository.get_by_account(db, account.account_number)
            if not existing_high_risk:
                high_risk = HighRiskAccount(
                    account_number=account.account_number,
                    high_risk_flag=1,
                    overall_risk_score=80,
                    risk_source="rules_engine",
                    risk_reason="Triggered AML rules",
                    detected_date=utc_now(),
                )
                HighRiskAccountRepository.create(db, high_risk)

            # --- Pick highest-priority alert and run agent once ---
            severity_priority = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            primary_alert = min(alerts, key=lambda a: severity_priority.get(a.severity, 99))
            logger.info(
                f"[TRACE] TransactionService | primary alert selected | "
                f"alert_id={primary_alert.alert_id} severity={primary_alert.severity} "
                f"type={primary_alert.alert_type} | skipped {len(alerts) - 1} lower-priority alerts"
            )

            t_agent_init = time.perf_counter()
            logger.info(f"[TRACE] TransactionService | MasterAgent init START")
            master_agent = MasterAgent()
            elapsed_init = round((time.perf_counter() - t_agent_init) * 1000, 2)
            logger.info(f"[TRACE] TransactionService | MasterAgent init END | {elapsed_init}ms")

            t_alert = time.perf_counter()
            logger.info(f"[TRACE] TransactionService | MasterAgent.run_for_alert START | alert_id={primary_alert.alert_id}")
            master_agent.run_for_alert(db, primary_alert.alert_id)
            elapsed_alert = round((time.perf_counter() - t_alert) * 1000, 2)
            logger.info(f"[TRACE] TransactionService | MasterAgent.run_for_alert END | {elapsed_alert}ms")

            elapsed_total = round((time.perf_counter() - t0) * 1000, 2)
            logger.info(f"[TRACE] TransactionService | create_transaction END (held) | txn={transaction.transaction_id} | {elapsed_total}ms")
            return transaction

        transaction.transaction_status = "completed"
        TransactionRepository.update(db, transaction)

        if transaction.transaction_type in {"deposit", "trade-sell"}:
            account.balance_amount += transaction.transaction_amount
        else:
            account.balance_amount -= transaction.transaction_amount
        AccountRepository.update(db, account)

        elapsed_total = round((time.perf_counter() - t0) * 1000, 2)
        logger.info(f"[TRACE] TransactionService | create_transaction END (completed) | txn={transaction.transaction_id} | {elapsed_total}ms")
        return transaction

    @staticmethod
    def list_transactions(
        db: Session,
        page: int,
        page_size: int,
        account_number: str | None = None,
        transaction_type: str | None = None,
        transaction_status: str | None = None,
    ) -> tuple[list[Transaction], int]:
        offset = (page - 1) * page_size
        items = TransactionRepository.list(
            db,
            offset=offset,
            limit=page_size,
            account_number=account_number,
            transaction_type=transaction_type,
            transaction_status=transaction_status,
        )
        total = TransactionRepository.count(
            db,
            account_number=account_number,
            transaction_type=transaction_type,
            transaction_status=transaction_status,
        )
        return items, total

    @staticmethod
    def list_transactions_by_account(
        db: Session, account_number: str, page: int, page_size: int
    ) -> tuple[list[Transaction], int]:
        offset = (page - 1) * page_size
        items = TransactionRepository.list(db, offset=offset, limit=page_size, account_number=account_number)
        total = TransactionRepository.count(db, account_number=account_number)
        return items, total

    @staticmethod
    def get_transaction(db: Session, transaction_id: str) -> Transaction:
        transaction = TransactionRepository.get_by_id(db, transaction_id)
        if not transaction:
            raise NotFoundException(TRANSACTION_NOT_FOUND, "Transaction not found")
        return transaction
