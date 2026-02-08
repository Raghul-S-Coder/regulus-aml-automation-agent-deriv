import time

from loguru import logger
from pydantic import BaseModel

from app.agents.state import AMLAnalysisState


class ContextualOutput(BaseModel):
    score: float
    summary: str


def analyze(state: AMLAnalysisState, llm) -> dict:
    logger.info("[TRACE] Agent:contextual | analyze START")
    if llm is None:
        logger.info("[TRACE] Agent:contextual | LLM is None (stub mode) | skipped")
        return {"contextual_score": 50.0, "contextual_summary": "LLM not configured"}

    prompt = (
        "You are a contextual risk scorer. Assess holistic risk given KYC/risk rating and transaction context. "
        "Return a score 0-100 and a short summary.\n\n"
        f"Customer: {state['customer_profile']}\n"
        f"Account: {state['account_info']}\n"
        f"Current transaction: {state['current_transaction']}\n"
        f"High risk info: {state['high_risk_info']}\n"
    )

    model = llm.with_structured_output(ContextualOutput)
    t0 = time.perf_counter()
    logger.info("[TRACE] Agent:contextual | LLM call START")
    result: ContextualOutput = model.invoke(prompt)
    elapsed = round((time.perf_counter() - t0) * 1000, 2)
    logger.info(f"[TRACE] Agent:contextual | LLM call END | score={result.score} | {elapsed}ms")
    return {"contextual_score": result.score, "contextual_summary": result.summary}
