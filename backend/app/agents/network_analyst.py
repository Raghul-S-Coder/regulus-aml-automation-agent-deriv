import time

from loguru import logger
from pydantic import BaseModel

from app.agents.state import AMLAnalysisState


class NetworkOutput(BaseModel):
    score: float
    summary: str


def analyze(state: AMLAnalysisState, llm) -> dict:
    logger.info("[TRACE] Agent:network | analyze START")
    if llm is None:
        logger.info("[TRACE] Agent:network | LLM is None (stub mode) | skipped")
        return {"network_score": 50.0, "network_summary": "LLM not configured"}

    prompt = (
        "You are a network analyst. Look for relationships across accounts/devices/IPs (if present). "
        "Return a score 0-100 and a short summary.\n\n"
        f"Account: {state['account_info']}\n"
        f"Existing alerts: {state['existing_alerts']}\n"
        f"Transaction history (recent): {state['transaction_history']}\n"
    )

    model = llm.with_structured_output(NetworkOutput)
    t0 = time.perf_counter()
    logger.info("[TRACE] Agent:network | LLM call START")
    result: NetworkOutput = model.invoke(prompt)
    elapsed = round((time.perf_counter() - t0) * 1000, 2)
    logger.info(f"[TRACE] Agent:network | LLM call END | score={result.score} | {elapsed}ms")
    return {"network_score": result.score, "network_summary": result.summary}
