import time

from fastapi import APIRouter, Depends, Request
from loguru import logger
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.common import StandardHeaders, success_response
from app.schemas.simulation import SimulationRunRequest
from app.schemas.transaction import TransactionOut
from app.services.simulation_service import SimulationService
from app.utils.datetime_utils import utc_now

router = APIRouter()


@router.get("/scenarios", response_model=dict)
def list_scenarios(
    request: Request,
    _headers: StandardHeaders = Depends(),
):
    scenarios = [s.model_dump() for s in SimulationService.list_scenarios()]
    return success_response(scenarios, request.state.request_id, utc_now().isoformat())


@router.post("/scenario", response_model=dict)
def run_scenario(
    payload: SimulationRunRequest,
    request: Request,
    account_number: str,
    _headers: StandardHeaders = Depends(),
    db: Session = Depends(get_db),
):
    start = time.perf_counter()
    logger.info(f"[TRACE] Controller | run_scenario START | scenario={payload.scenario_id} account={account_number}")
    txns = SimulationService.run_scenario(db, account_number, payload.scenario_id)
    data = [TransactionOut.model_validate(t).model_dump() for t in txns]
    elapsed = round((time.perf_counter() - start) * 1000, 2)
    logger.info(f"[TRACE] Controller | run_scenario END | {len(txns)} txns | {elapsed}ms")
    return success_response(data, request.state.request_id, utc_now().isoformat())


@router.post("/reset", response_model=dict)
def reset_data(
    request: Request,
    _headers: StandardHeaders = Depends(),
    db: Session = Depends(get_db),
):
    SimulationService.reset_data(db)
    return success_response({"status": "reset"}, request.state.request_id, utc_now().isoformat())
