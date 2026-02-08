import time

from loguru import logger
from pydantic import BaseModel

from app.agents.state import AMLAnalysisState


class BehavioralOutput(BaseModel):
    score: float
    summary: str


def analyze(state: AMLAnalysisState, llm) -> dict:
    logger.info("[TRACE] Agent:behavioral | analyze START")
    if llm is None:
        logger.info("[TRACE] Agent:behavioral | LLM is None (stub mode) | skipped")
        return {"behavioral_score": 50.0, "behavioral_summary": "LLM not configured"}

    prompt = (
        "You are a behavioral analyst. Analyze if the current transaction deviates from historical behavior. "
        "Return a score 0-100 and a short summary.\n\n"
        f"Customer: {state['customer_profile']}\n"
        f"Account: {state['account_info']}\n"
        f"Current transaction: {state['current_transaction']}\n"
        f"Transaction history (recent): {state['transaction_history']}\n"
    )

    model = llm.with_structured_output(BehavioralOutput)
    t0 = time.perf_counter()
    logger.info("[TRACE] Agent:behavioral | LLM call START")
    result: BehavioralOutput = model.invoke(prompt)
    elapsed = round((time.perf_counter() - t0) * 1000, 2)
    logger.info(f"[TRACE] Agent:behavioral | LLM call END | score={result.score} | {elapsed}ms")
    return {"behavioral_score": result.score, "behavioral_summary": result.summary}
