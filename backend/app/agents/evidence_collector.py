import time

from loguru import logger
from pydantic import BaseModel

from app.agents.state import AMLAnalysisState


class EvidenceOutput(BaseModel):
    score: float
    summary: str


def analyze(state: AMLAnalysisState, llm) -> dict:
    logger.info("[TRACE] Agent:evidence | analyze START")
    if llm is None:
        logger.info("[TRACE] Agent:evidence | LLM is None (stub mode) | skipped")
        return {"evidence_score": 50.0, "evidence_summary": "LLM not configured"}

    prompt = (
        "You are an evidence collector. Build an evidence summary and score suspicious indicators. "
        "Return a score 0-100 and a concise summary.\n\n"
        f"Current transaction: {state['current_transaction']}\n"
        f"Existing alerts: {state['existing_alerts']}\n"
        f"Transaction history (recent): {state['transaction_history']}\n"
        f"Behavioral summary: {state.get('behavioral_summary')}\n"
        f"Network summary: {state.get('network_summary')}\n"
        f"Contextual summary: {state.get('contextual_summary')}\n"
    )

    model = llm.with_structured_output(EvidenceOutput)
    t0 = time.perf_counter()
    logger.info("[TRACE] Agent:evidence | LLM call START")
    result: EvidenceOutput = model.invoke(prompt)
    elapsed = round((time.perf_counter() - t0) * 1000, 2)
    logger.info(f"[TRACE] Agent:evidence | LLM call END | score={result.score} | {elapsed}ms")
    return {"evidence_score": result.score, "evidence_summary": result.summary}
