import time

from loguru import logger
from pydantic import BaseModel

from app.agents.state import AMLAnalysisState


class DocumentOutput(BaseModel):
    content: str


def generate(state: AMLAnalysisState, llm) -> dict:
    logger.info("[TRACE] Agent:document | generate START")
    if llm is None:
        logger.info("[TRACE] Agent:document | LLM is None (stub mode) | skipped")
        return {"document_content": "LLM not configured"}

    prompt = (
        "You are a SAR document generator. Produce a concise narrative suitable for a SAR draft. "
        "Use the case summary and evidence.\n\n"
        f"Case summary: {state.get('case_summary')}\n"
        f"Behavioral: {state.get('behavioral_summary')}\n"
        f"Network: {state.get('network_summary')}\n"
        f"Contextual: {state.get('contextual_summary')}\n"
        f"Evidence: {state.get('evidence_summary')}\n"
        f"False positive: {state.get('false_positive_summary')}\n"
    )

    model = llm.with_structured_output(DocumentOutput)
    t0 = time.perf_counter()
    logger.info("[TRACE] Agent:document | LLM call START")
    result: DocumentOutput = model.invoke(prompt)
    elapsed = round((time.perf_counter() - t0) * 1000, 2)
    logger.info(f"[TRACE] Agent:document | LLM call END | {elapsed}ms")
    return {"document_content": result.content}
