import time

from loguru import logger
from pydantic import BaseModel

from app.agents.state import AMLAnalysisState


class FalsePositiveOutput(BaseModel):
    score: float
    summary: str


def analyze(state: AMLAnalysisState, llm) -> dict:
    logger.info("[TRACE] Agent:false_positive | analyze START")
    if llm is None:
        logger.info("[TRACE] Agent:false_positive | LLM is None (stub mode) | skipped")
        return {"false_positive_score": 50.0, "false_positive_summary": "LLM not configured"}

    prompt = (
        "You are a false positive optimizer. Given all prior analyses, estimate likelihood of false positive. "
        "Return a score 0-100 (higher means less likely false positive) and a short summary.\n\n"
        f"Behavioral score/summary: {state.get('behavioral_score')} / {state.get('behavioral_summary')}\n"
        f"Network score/summary: {state.get('network_score')} / {state.get('network_summary')}\n"
        f"Contextual score/summary: {state.get('contextual_score')} / {state.get('contextual_summary')}\n"
        f"Evidence score/summary: {state.get('evidence_score')} / {state.get('evidence_summary')}\n"
        f"High risk info: {state['high_risk_info']}\n"
    )

    model = llm.with_structured_output(FalsePositiveOutput)
    t0 = time.perf_counter()
    logger.info("[TRACE] Agent:false_positive | LLM call START")
    result: FalsePositiveOutput = model.invoke(prompt)
    elapsed = round((time.perf_counter() - t0) * 1000, 2)
    logger.info(f"[TRACE] Agent:false_positive | LLM call END | score={result.score} | {elapsed}ms")
    return {"false_positive_score": result.score, "false_positive_summary": result.summary}
