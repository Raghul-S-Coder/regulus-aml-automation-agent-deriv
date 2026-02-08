import time
from datetime import timedelta

from loguru import logger
from sqlalchemy.orm import Session

from app.config.database import Base
from app.config.settings import settings
from app.exceptions.base_exception import NotFoundException
from app.exceptions.error_codes import SIMULATION_SCENARIO_NOT_FOUND
from app.schemas.simulation import SimulationScenario
from app.schemas.transaction import TransactionCreate
from app.services.transaction_service import TransactionService
from app.utils.datetime_utils import utc_now


class SimulationService:
    _SCENARIOS: dict[str, SimulationScenario] = {
        "high_deposit": SimulationScenario(
            scenario_id="high_deposit",
            name="High Amount Deposit",
            description="Creates a deposit above the configured threshold",
        ),
        "negligible_profit": SimulationScenario(
            scenario_id="negligible_profit",
            name="Negligible Profit Trade",
            description="Deposit, trade-buy, trade-sell with negligible profit",
        ),
        "rapid_cycle": SimulationScenario(
            scenario_id="rapid_cycle",
            name="Rapid Deposit-Withdrawal",
            description="Deposit followed by withdrawal within a short window",
        ),
        "velocity_burst": SimulationScenario(
            scenario_id="velocity_burst",
            name="Transaction Velocity Burst",
            description="Multiple rapid deposits in a short window",
        ),
        "cross_border": SimulationScenario(
            scenario_id="cross_border",
            name="Cross-Border Deposit",
            description="Deposit from a country different than customer residency",
        ),
        "clean_transaction": SimulationScenario(
            scenario_id="clean_transaction",
            name="Normal Transaction",
            description="Legitimate deposit below thresholds",
        ),
    }

    @staticmethod
    def list_scenarios() -> list[SimulationScenario]:
        return list(SimulationService._SCENARIOS.values())

    @staticmethod
    def _create_and_log(db, payload, index, total):
        start = time.perf_counter()
        logger.info(f"[TRACE] SimulationService | creating txn {index}/{total} | type={payload.transaction_type} amount={payload.transaction_amount}")
        txn = TransactionService.create_transaction(db, payload)
        elapsed = round((time.perf_counter() - start) * 1000, 2)
        logger.info(f"[TRACE] SimulationService | txn {index}/{total} done | id={txn.transaction_id} status={txn.transaction_status} | {elapsed}ms")
        return txn

    @staticmethod
    def run_scenario(db: Session, account_number: str, scenario_id: str):
        if scenario_id not in SimulationService._SCENARIOS:
            raise NotFoundException(SIMULATION_SCENARIO_NOT_FOUND, "Scenario not found")

        start = time.perf_counter()
        logger.info(f"[TRACE] SimulationService | run_scenario START | scenario={scenario_id} account={account_number}")

        now = utc_now()
        if scenario_id == "high_deposit":
            payload = TransactionCreate(
                account_number=account_number,
                transaction_amount=50000.0,
                transaction_currency="USD",
                transaction_date=now,
                transaction_type="deposit",
                deposit_source_country="US",
            )
            result = [SimulationService._create_and_log(db, payload, 1, 1)]
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            logger.info(f"[TRACE] SimulationService | run_scenario END | scenario={scenario_id} | {elapsed}ms")
            return result

        if scenario_id == "negligible_profit":
            deposit = TransactionCreate(
                account_number=account_number,
                transaction_amount=500.0,
                transaction_currency="USD",
                transaction_date=now,
                transaction_type="deposit",
                deposit_source_country="US",
            )
            buy = TransactionCreate(
                account_number=account_number,
                transaction_amount=500.0,
                transaction_currency="USD",
                transaction_date=now + timedelta(minutes=5),
                transaction_type="trade-buy",
            )
            sell = TransactionCreate(
                account_number=account_number,
                transaction_amount=500.01,
                transaction_currency="USD",
                transaction_date=now + timedelta(minutes=10),
                transaction_type="trade-sell",
            )
            result = [
                SimulationService._create_and_log(db, deposit, 1, 3),
                SimulationService._create_and_log(db, buy, 2, 3),
                SimulationService._create_and_log(db, sell, 3, 3),
            ]
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            logger.info(f"[TRACE] SimulationService | run_scenario END | scenario={scenario_id} | {elapsed}ms")
            return result

        if scenario_id == "rapid_cycle":
            deposit = TransactionCreate(
                account_number=account_number,
                transaction_amount=5000.0,
                transaction_currency="USD",
                transaction_date=now,
                transaction_type="deposit",
                deposit_source_country="US",
            )
            withdrawal = TransactionCreate(
                account_number=account_number,
                transaction_amount=4950.0,
                transaction_currency="USD",
                transaction_date=now + timedelta(minutes=30),
                transaction_type="withdrawal",
            )
            result = [
                SimulationService._create_and_log(db, deposit, 1, 2),
                SimulationService._create_and_log(db, withdrawal, 2, 2),
            ]
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            logger.info(f"[TRACE] SimulationService | run_scenario END | scenario={scenario_id} | {elapsed}ms")
            return result

        if scenario_id == "velocity_burst":
            txns = []
            count = min(settings.SIMULATION_MAX_TXN_PER_SCENARIO, 6)
            for i in range(count):
                payload = TransactionCreate(
                    account_number=account_number,
                    transaction_amount=200.0,
                    transaction_currency="USD",
                    transaction_date=now + timedelta(minutes=i * 5),
                    transaction_type="deposit",
                    deposit_source_country="US",
                )
                txns.append(SimulationService._create_and_log(db, payload, i + 1, count))
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            logger.info(f"[TRACE] SimulationService | run_scenario END | scenario={scenario_id} | {elapsed}ms")
            return txns

        if scenario_id == "cross_border":
            payload = TransactionCreate(
                account_number=account_number,
                transaction_amount=3000.0,
                transaction_currency="USD",
                transaction_date=now,
                transaction_type="deposit",
                deposit_source_country="GB",
            )
            result = [SimulationService._create_and_log(db, payload, 1, 1)]
            elapsed = round((time.perf_counter() - start) * 1000, 2)
            logger.info(f"[TRACE] SimulationService | run_scenario END | scenario={scenario_id} | {elapsed}ms")
            return result

        payload = TransactionCreate(
            account_number=account_number,
            transaction_amount=200.0,
            transaction_currency="USD",
            transaction_date=now,
            transaction_type="deposit",
            deposit_source_country="US",
        )
        result = [SimulationService._create_and_log(db, payload, 1, 1)]
        elapsed = round((time.perf_counter() - start) * 1000, 2)
        logger.info(f"[TRACE] SimulationService | run_scenario END | scenario={scenario_id} | {elapsed}ms")
        return result

    @staticmethod
    def reset_data(db: Session) -> None:
        """Delete all data from all tables (SQLite reset)."""
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()
