import time

from langgraph.graph import END, StateGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from loguru import logger
from sqlalchemy.orm import Session

from app.agents.behavioral_analyst import analyze as behavioral_analyze
from app.agents.contextual_scorer import analyze as contextual_analyze
from app.agents.document_generator import generate as document_generate
from app.agents.evidence_collector import analyze as evidence_analyze
from app.agents.false_positive_optimizer import analyze as false_positive_analyze
from app.agents.network_analyst import analyze as network_analyze
from app.agents.state import AMLAnalysisState
from app.agents.tools import (
    get_account,
    get_alerts,
    get_customer,
    get_high_risk_info,
    get_latest_transaction,
    get_transaction_history,
)
from app.config.settings import settings
from app.exceptions.base_exception import AMLException, NotFoundException
from app.exceptions.error_codes import AGENT_LLM_API_FAILED, ALERT_NOT_FOUND
from app.models.alert import Alert
from app.models.case import Case
from app.models.case_document_content import CaseDocumentContent
from app.repositories.case_repository import CaseRepository
from app.utils.datetime_utils import utc_now
from app.utils.id_generator import generate_id


class MasterAgent:
    def __init__(self) -> None:
        t0 = time.perf_counter()
        self.llm = self._build_llm()
        elapsed_llm = round((time.perf_counter() - t0) * 1000, 2)
        provider = settings.LLM_PROVIDER
        model = settings.GEMINI_MODEL if provider == "gemini" else settings.OPENAI_MODEL
        logger.info(f"[TRACE] MasterAgent | LLM initialized | provider={provider} model={model} | stub={self.llm is None} | {elapsed_llm}ms")

        t1 = time.perf_counter()
        self.graph = self._build_graph()
        elapsed_graph = round((time.perf_counter() - t1) * 1000, 2)
        logger.info(f"[TRACE] MasterAgent | Graph built | {elapsed_graph}ms")

    def _build_llm(self):
        provider = settings.LLM_PROVIDER.lower()

        if provider == "gemini":
            api_key = settings.GEMINI_API_KEY
            model = settings.GEMINI_MODEL
            if not api_key or api_key == "your-gemini-key-here":
                logger.warning("Gemini API key not configured; running in stub mode")
                return None
            try:
                logger.info(f"[TRACE] MasterAgent | Initializing Gemini LLM | model={model}")
                return ChatGoogleGenerativeAI(model=model, api_key=api_key)
            except Exception as exc:
                raise AMLException(AGENT_LLM_API_FAILED, f"Failed to initialize Gemini LLM: {exc}") from exc

        if provider == "openai":
            api_key = settings.OPENAI_API_KEY
            model = settings.OPENAI_MODEL
            if not api_key or api_key == "your-openai-key-here":
                logger.warning("OpenAI API key not configured; running in stub mode")
                return None
            try:
                logger.info(f"[TRACE] MasterAgent | Initializing OpenAI LLM | model={model}")
                return ChatOpenAI(model=model, api_key=api_key)
            except Exception as exc:
                raise AMLException(AGENT_LLM_API_FAILED, f"Failed to initialize OpenAI LLM: {exc}") from exc

        raise AMLException(AGENT_LLM_API_FAILED, f"Unsupported LLM_PROVIDER: '{provider}'. Use 'gemini' or 'openai'.")

    def _build_graph(self):
        graph = StateGraph(AMLAnalysisState)

        graph.add_node("behavioral", lambda state: behavioral_analyze(state, self.llm))
        graph.add_node("network", lambda state: network_analyze(state, self.llm))
        graph.add_node("contextual", lambda state: contextual_analyze(state, self.llm))
        graph.add_node("evidence", lambda state: evidence_analyze(state, self.llm))
        graph.add_node("false_positive", lambda state: false_positive_analyze(state, self.llm))
        graph.add_node("finalize", self._finalize_case)
        graph.add_node("document", lambda state: document_generate(state, self.llm))

        graph.set_entry_point("behavioral")
        graph.add_edge("behavioral", "network")
        graph.add_edge("network", "contextual")
        graph.add_edge("contextual", "evidence")
        graph.add_edge("evidence", "false_positive")
        graph.add_edge("false_positive", "finalize")
        graph.add_edge("finalize", "document")
        graph.add_edge("document", END)

        return graph.compile()

    def _finalize_case(self, state: AMLAnalysisState) -> dict:
        logger.info("[TRACE] MasterAgent | finalize_case START")
        case_score = (
            state.get("behavioral_score", 0.0) * 0.25
            + state.get("network_score", 0.0) * 0.20
            + state.get("contextual_score", 0.0) * 0.20
            + state.get("evidence_score", 0.0) * 0.20
            + state.get("false_positive_score", 0.0) * 0.15
        )

        if case_score < 20:
            classification = "false_positive"
        elif case_score < 50:
            classification = "low"
        elif case_score < 75:
            classification = "medium"
        else:
            classification = "high"

        case_summary = (
            f"Classification: {classification}. "
            f"Behavioral: {state.get('behavioral_summary')}. "
            f"Network: {state.get('network_summary')}. "
            f"Contextual: {state.get('contextual_summary')}. "
            f"Evidence: {state.get('evidence_summary')}."
        )

        logger.info(f"[TRACE] MasterAgent | finalize_case END | score={round(case_score, 2)} classification={classification}")

        return {
            "case_score_percentage": round(case_score, 2),
            "case_classification": classification,
            "case_summary": case_summary,
        }

    def run_for_alert(self, db: Session, alert_id: str) -> Case:
        t0 = time.perf_counter()
        logger.info(f"[TRACE] MasterAgent | run_for_alert START | alert_id={alert_id}")

        alert = db.query(Alert).filter(Alert.alert_id == alert_id).first()
        if not alert:
            raise NotFoundException(ALERT_NOT_FOUND, "Alert not found")

        # --- Data fetching ---
        t_fetch = time.perf_counter()
        logger.info(f"[TRACE] MasterAgent | data fetch START | account={alert.account_number}")
        account = get_account(db, alert.account_number)
        if not account:
            raise NotFoundException(ALERT_NOT_FOUND, "Alert account not found")

        customer = get_customer(db, account.customer_id)
        current_txn = get_latest_transaction(db, alert.account_number)
        tx_history = get_transaction_history(db, alert.account_number)
        existing_alerts = get_alerts(db, alert.account_number)
        high_risk = get_high_risk_info(db, alert.account_number)
        elapsed_fetch = round((time.perf_counter() - t_fetch) * 1000, 2)
        logger.info(
            f"[TRACE] MasterAgent | data fetch END | "
            f"txn_history={len(tx_history)} alerts={len(existing_alerts)} high_risk={'yes' if high_risk else 'no'} | {elapsed_fetch}ms"
        )

        initial_state: AMLAnalysisState = {
            "alert_id": alert.alert_id,
            "account_number": alert.account_number,
            "transaction_id": current_txn.transaction_id if current_txn else "",
            "customer_profile": customer.__dict__ if customer else {},
            "account_info": account.__dict__,
            "transaction_history": [t.__dict__ for t in tx_history],
            "current_transaction": current_txn.__dict__ if current_txn else {},
            "existing_alerts": [a.__dict__ for a in existing_alerts],
            "high_risk_info": high_risk.__dict__ if high_risk else None,
            "behavioral_score": 0.0,
            "behavioral_summary": "",
            "network_score": 0.0,
            "network_summary": "",
            "contextual_score": 0.0,
            "contextual_summary": "",
            "evidence_score": 0.0,
            "evidence_summary": "",
            "false_positive_score": 0.0,
            "false_positive_summary": "",
            "case_score_percentage": 0.0,
            "case_classification": "",
            "case_summary": "",
            "document_content": "",
        }

        # --- Graph execution ---
        t_graph = time.perf_counter()
        logger.info(f"[TRACE] MasterAgent | graph.invoke START | alert_id={alert_id}")
        result: AMLAnalysisState = self.graph.invoke(initial_state)
        elapsed_graph = round((time.perf_counter() - t_graph) * 1000, 2)
        logger.info(f"[TRACE] MasterAgent | graph.invoke END | score={result.get('case_score_percentage')} | {elapsed_graph}ms")

        # --- Case creation ---
        case = Case(
            case_id=generate_id("CASE"),
            alert_id=alert.alert_id,
            account_number=alert.account_number,
            transaction_id=alert.transaction_id,
            case_status="OPEN",
            case_score_percentage=result.get("case_score_percentage", 0.0),
            behavoir_agent_score=result.get("behavioral_score"),
            behavoir_agent_summary=result.get("behavioral_summary"),
            network_agent_score=result.get("network_score"),
            network_agent_summary=result.get("network_summary"),
            contextual_agent_score=result.get("contextual_score"),
            contextual_agent_summary=result.get("contextual_summary"),
            evidence_agent_score=result.get("evidence_score"),
            evidence_agent_summary=result.get("evidence_summary"),
            false_positive_agent_score=result.get("false_positive_score"),
            false_positive_agent_summary=result.get("false_positive_summary"),
            case_opened_date=utc_now(),
            case_summary=result.get("case_summary", ""),
        )
        case = CaseRepository.create_case(db, case)

        document = CaseDocumentContent(
            document_id=generate_id("DOC"),
            case_id=case.case_id,
            content_type="sar_draft",
            content=result.get("document_content", ""),
            generated_by="document_generator_agent",
            version=1,
        )
        CaseRepository.create_document(db, document)

        elapsed_total = round((time.perf_counter() - t0) * 1000, 2)
        logger.info(f"[TRACE] MasterAgent | run_for_alert END | alert_id={alert_id} case_id={case.case_id} | {elapsed_total}ms")

        return case
