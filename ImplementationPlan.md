# AML Transaction Monitoring System - Implementation Plan (Backend + Frontend)

## Project Structure

```
RegulusAI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                          # FastAPI app factory
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   ├── settings.py                  # Pydantic BaseSettings (.env loader)
│   │   │   └── database.py                  # SQLAlchemy engine, session, Base
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── request_context.py           # UUID, X-Forwarded-For, X-Device-Id, loguru context
│   │   ├── models/                          # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── organization.py
│   │   │   ├── user.py
│   │   │   ├── customer.py
│   │   │   ├── account.py
│   │   │   ├── high_risk_account.py
│   │   │   ├── transaction.py
│   │   │   ├── alert.py
│   │   │   ├── case.py
│   │   │   ├── case_document_content.py
│   │   │   └── case_decision.py
│   │   ├── schemas/                         # Pydantic request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── common.py                    # Standard headers, pagination, error response
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── customer.py
│   │   │   ├── account.py
│   │   │   ├── transaction.py
│   │   │   ├── alert.py
│   │   │   ├── case.py
│   │   │   └── simulation.py
│   │   ├── controllers/                     # FastAPI routers (one per module)
│   │   │   ├── __init__.py
│   │   │   ├── auth_controller.py
│   │   │   ├── user_controller.py
│   │   │   ├── customer_controller.py
│   │   │   ├── account_controller.py
│   │   │   ├── transaction_controller.py
│   │   │   ├── alert_controller.py
│   │   │   ├── case_controller.py
│   │   │   └── simulation_controller.py
│   │   ├── services/                        # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── customer_service.py
│   │   │   ├── account_service.py
│   │   │   ├── transaction_service.py
│   │   │   ├── alert_service.py
│   │   │   ├── case_service.py
│   │   │   └── simulation_service.py
│   │   ├── repositories/                    # Database access layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_repository.py
│   │   │   ├── user_repository.py
│   │   │   ├── customer_repository.py
│   │   │   ├── account_repository.py
│   │   │   ├── transaction_repository.py
│   │   │   ├── alert_repository.py
│   │   │   ├── case_repository.py
│   │   │   └── high_risk_account_repository.py
│   │   ├── rules/                           # AML rules engine
│   │   │   ├── __init__.py
│   │   │   ├── rule_engine.py               # Orchestrator: evaluates all rules
│   │   │   ├── base_rule.py                 # Abstract base class for rules
│   │   │   ├── high_deposit_rule.py         # RULE-01: High amount deposit
│   │   │   ├── negligible_profit_rule.py    # RULE-02: Negligible profit/loss trade
│   │   │   ├── rapid_cycle_rule.py          # RULE-03: Rapid deposit-withdrawal
│   │   │   ├── velocity_rule.py             # RULE-04: Multiple transactions in short time
│   │   │   ├── cross_border_rule.py         # RULE-05: Cross-border source mismatch
│   │   │   └── high_risk_account_rule.py    # RULE-06: Account in high risk table
│   │   ├── agents/                          # LangGraph AI agents
│   │   │   ├── __init__.py
│   │   │   ├── master_agent.py              # AML Analyst - LangGraph supervisor
│   │   │   ├── behavioral_analyst.py        # Behavioral pattern analysis
│   │   │   ├── network_analyst.py           # Network/graph analysis
│   │   │   ├── contextual_scorer.py         # Contextual risk scoring
│   │   │   ├── evidence_collector.py        # Evidence collection & timeline
│   │   │   ├── false_positive_optimizer.py  # False positive reduction
│   │   │   ├── document_generator.py        # SAR document content generation
│   │   │   ├── state.py                     # LangGraph shared state definition
│   │   │   └── tools.py                     # Agent tools (DB queries, etc.)
│   │   ├── exceptions/
│   │   │   ├── __init__.py
│   │   │   ├── error_codes.py               # All AML error code constants
│   │   │   ├── base_exception.py            # Custom exception classes
│   │   │   └── handlers.py                  # Global exception handlers
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── id_generator.py              # Generate CUST-XXXX, ACC-XXXX, etc.
│   │       └── datetime_utils.py            # UTC timestamp helpers
│   ├── seeds/
│   │   ├── seed_runner.py
│   │   ├── seed_organizations.py
│   │   ├── seed_users.py
│   │   ├── seed_customers.py
│   │   └── seed_accounts.py
        --- seed_transactions.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_customers.py
│   │   ├── test_accounts.py
│   │   ├── test_transactions.py
│   │   ├── test_rules_engine.py
│   │   ├── test_agents.py
│   │   └── test_integration/
│   │       └── test_end_to_end.py
│   ├── .env                                 # Environment variables
│   ├── .env.example                         # Template
│   ├── requirements.txt
│   ├── pyproject.toml                       # Linting config (ruff)
│   └── README.md
└── frontend/
    ├── index.html
    ├── package.json
    ├── postcss.config.cjs
    ├── tailwind.config.ts
    ├── tsconfig.json
    ├── tsconfig.node.json
    ├── vite.config.ts
    ├── QA_CHECKLIST.md
    └── src/
        ├── App.tsx
        ├── main.tsx
        ├── styles/
        │   └── globals.css
        ├── lib/
        │   └── utils.ts
        └── app/
            ├── api/
            │   ├── auth.ts
            │   ├── client.ts
            │   └── simulation.ts
            ├── components/
            │   ├── States.tsx
            │   ├── ThemeToggle.tsx
            │   └── WorkflowGraphic.tsx
            ├── hooks/
            │   ├── useApi.ts
            │   ├── useAuth.ts
            │   └── useTheme.ts
            ├── layouts/
            │   ├── MonitoringLayout.tsx
            │   └── PublicLayout.tsx
            ├── pages/
            │   ├── AlertsPage.tsx
            │   ├── CaseDetailsPage.tsx
            │   ├── CasesPage.tsx
            │   ├── DashboardPage.tsx
            │   ├── HomePage.tsx
            │   ├── LoginPage.tsx
            │   ├── TransactionDemoPage.tsx
            │   └── TransactionsPage.tsx
            └── routes.tsx
```

---

## Frontend Status (Implemented)

The frontend is now scaffolded in `frontend/` with React + TypeScript + Tailwind and emerald theming. Core pages and routes are implemented:
`/regulus`, `/regulus/login`, `/regulus/transaction-demo`, `/regulus/monitoring/*` (Dashboard, Transactions, Alerts, Cases, Case Details).
See `FrontendImplementationPlan.md` for the phase-by-phase UI plan and `frontend/QA_CHECKLIST.md` for QA steps.

---

## Phase 1: Project Setup & Infrastructure

### What Gets Built
- Project directory structure
- Python virtual environment and dependency management
- `.env` configuration with Pydantic BaseSettings
- Loguru logging with request-context injection (UUID, timestamp, source, message)
- Linting setup with Ruff

### Files to Create
- `backend/requirements.txt` - Dependencies: fastapi, uvicorn, sqlalchemy, pydantic-settings, loguru, langgraph, langchain-openai, python-dotenv, httpx, ruff, pytest, bcrypt
- `backend/pyproject.toml` - Ruff linting configuration
- `backend/.env` and `.env.example` - Configuration values
- `backend/app/__init__.py`
- `backend/app/config/__init__.py`
- `backend/app/config/settings.py` - Pydantic BaseSettings class

### Key Design Decisions
- **Settings class** loads from `.env` with defaults: `DEPOSIT_THRESHOLD=10000.0`, `NEGLIGIBLE_PROFIT_THRESHOLD=1.0`, `RAPID_CYCLE_HOURS=24`, `VELOCITY_TXN_COUNT=5`, `VELOCITY_WINDOW_MINUTES=60`, `DB_URL=sqlite:///./regulus_aml.db`, `LLM_MODEL`, `LLM_API_KEY`
- **Loguru** configured with custom format: `{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {extra[request_id]} | {name}:{line} | {message}`
- All business thresholds are configurable via `.env`, never hardcoded

### Business Configuration Values (.env)
```
DATABASE_URL=sqlite:///./regulus_aml.db
DEPOSIT_THRESHOLD=10000.0
NEGLIGIBLE_PROFIT_THRESHOLD=1.0
RAPID_CYCLE_HOURS=24
VELOCITY_TXN_COUNT=5
VELOCITY_WINDOW_MINUTES=60
CROSS_BORDER_ALERT_SEVERITY=high
LLM_MODEL=gemini-2.5-flash
LLM_API_KEY=your-key-here
LOG_LEVEL=DEBUG
```

---

## Phase 2: Database Layer

### What Gets Built
- SQLAlchemy engine and session configuration for SQLite
- All 10 ORM models matching DatabaseModel.md schema exactly
- Database initialization (create_all)

### Files to Create
- `backend/app/config/database.py` - Engine, SessionLocal, Base, `get_db` dependency, `init_db()`
- `backend/app/models/__init__.py` - Import all models
- `backend/app/models/organization.py`
- `backend/app/models/user.py`
- `backend/app/models/customer.py`
- `backend/app/models/account.py`
- `backend/app/models/high_risk_account.py`
- `backend/app/models/transaction.py`
- `backend/app/models/alert.py`
- `backend/app/models/case.py`
- `backend/app/models/case_document_content.py`
- `backend/app/models/case_decision.py`

### Table Schemas (exact column names from DatabaseModel.md)

**Organizations** (new - not in DatabaseModel.md):
| Column | Type | Notes |
|--------|------|-------|
| organization_id | String PK | Format: ORG-XXXX |
| name | String | |
| country | String | |
| status | String | active/inactive |
| created_date, updated_date | DateTime | |
| created_by, updated_by | String | |

**Users** (new - not in DatabaseModel.md):
| Column | Type | Notes |
|--------|------|-------|
| user_id | String PK | Format: USR-XXXX |
| organization_id | String FK | |
| username | String UNIQUE | |
| password_hash | String | bcrypt |
| full_name | String | |
| email | String | |
| user_type | String | compliance_manager / admin |
| is_active | Boolean | |
| created_date, updated_date | DateTime | |
| created_by, updated_by | String | |

**Customers** (from DatabaseModel.md):
| Column | Type |
|--------|------|
| customer_id | String PK (CUST-XXXXXX) |
| customer_type | String |
| full_name | String |
| date_of_birth | String |
| nationality | String |
| residency_country | String |
| id_type | String |
| id_number | String |
| phone | String |
| email | String |
| address_line1 | String |
| address_city | String |
| address_country | String |
| kyc_status | String |
| kyc_verified_date | String (nullable) |
| kyc_expired_date | String (nullable) |
| risk_rating | String |
| created_date, updated_date | DateTime |
| created_by, updated_by | String |

**Accounts** (from DatabaseModel.md):
| Column | Type |
|--------|------|
| customer_id | String FK |
| account_number | String PK (ACC-XXXXXXXXX) |
| account_type | String |
| account_status | String |
| opened_date | String |
| branch_code | String |
| balance_amount | Float |
| balance_currency | String |
| created_date, updated_date | DateTime |
| created_by, updated_by | String |

**High Risk Accounts** (from DatabaseModel.md):
| Column | Type |
|--------|------|
| id | Integer PK (auto) |
| account_number | String FK |
| high_risk_flag | Integer (0/1) |
| overall_risk_score | Integer |
| risk_source | String |
| risk_reason | String |
| detected_date | DateTime |
| created_date, updated_date | DateTime |
| created_by, updated_by | String |

**Transactions** (from DatabaseModel.md):
| Column | Type |
|--------|------|
| transaction_id | String PK (TXN-XXXXXXX) |
| account_number | String FK |
| transaction_amount | Float |
| transaction_currency | String |
| transaction_date | DateTime |
| transaction_type | String (deposit/withdrawal/trade-buy/trade-sell) |
| transaction_status | String (pending/completed/held/failed) |
| purpose | String (nullable) |
| deposit_source_type | String (nullable) |
| deposit_source_value | String (nullable) |
| deposit_source_country | String (nullable) |
| created_date, updated_date | DateTime |
| created_by, updated_by | String |

**Alerts** (from DatabaseModel.md):
| Column | Type |
|--------|------|
| alert_id | String PK (ALERT-XXXXXX) |
| account_number | String FK |
| alert_type | String |
| severity | String |
| rule_id | String |
| description | String |
| triggered_date | DateTime |
| created_date, updated_date | DateTime |
| created_by, updated_by | String |

**Cases** (from DatabaseModel.md):
| Column | Type |
|--------|------|
| case_id | String PK (CASE-XXXXXX) |
| alert_id | String FK |
| account_number | String FK |
| case_status | String (OPEN/CLOSE) |
| case_score_percentage | Float |
| behavoir_agent_score | Float (nullable) |
| behavoir_agent_summary | Text (nullable) |
| network_agent_score | Float (nullable) |
| network_agent_summary | Text (nullable) |
| contextual_agent_score | Float (nullable) |
| contextual_agent_summary | Text (nullable) |
| evidence_agent_score | Float (nullable) |
| evidence_agent_summary | Text (nullable) |
| false_positive_agent_score | Float (nullable) |
| false_positive_agent_summary | Text (nullable) |
| assigned_to | String (nullable) |
| assigned_date | DateTime (nullable) |
| case_opened_date | DateTime |
| case_closed_date | DateTime (nullable) |
| case_summary | Text |
| created_date, updated_date | DateTime |
| created_by, updated_by | String |

**Case Document Content** (new - not in DatabaseModel.md):
| Column | Type |
|--------|------|
| document_id | String PK (DOC-XXXXXX) |
| case_id | String FK |
| content_type | String (sar_draft/evidence_summary/timeline) |
| content | Text |
| generated_by | String (document_generator_agent) |
| version | Integer (default 1) |
| created_date, updated_date | DateTime |
| created_by, updated_by | String |

**Case Decisions** (from DatabaseModel.md):
| Column | Type |
|--------|------|
| id | Integer PK (auto) |
| case_id | String FK |
| decision | String (ACCEPT/REJECT) |
| decision_by | String |
| decision_date | DateTime |
| decision_reason | Text |
| next_action | String |
| created_date, updated_date | DateTime |
| created_by, updated_by | String |

### Key Design Decisions
- SQLite with `check_same_thread=False` for FastAPI async compatibility
- All ID columns use string-based formatted IDs (CUST-XXXXXX, ACC-XXXXXXXXX, etc.)
- Column names match DatabaseModel.md exactly (e.g., `behavoir_agent_score` not `behavior_agent_score`)
- Audit columns (created_date, updated_date, created_by, updated_by) on every table

### Dependencies
Phase 1 (settings for DB_URL)

---

## Phase 3: Core API Framework

### What Gets Built
- FastAPI application factory with CORS, routers, startup events
- Request context middleware (UUID, IP, Device ID extraction + loguru binding)
- Global exception handlers with unique error codes
- Standard request/response schemas
- ID generator utility

### Files to Create
- `backend/app/main.py` - `create_app()` factory
- `backend/app/middleware/request_context.py` - Middleware for header extraction + logging
- `backend/app/exceptions/error_codes.py` - Error code constants
- `backend/app/exceptions/base_exception.py` - Custom AMLException class
- `backend/app/exceptions/handlers.py` - Global handlers registered on app
- `backend/app/schemas/common.py` - StandardHeaders, ErrorResponse, PaginatedResponse
- `backend/app/utils/id_generator.py` - `generate_id(prefix, sequence)`
- `backend/app/utils/datetime_utils.py` - `utc_now()` helper

### Error Code Registry

| Range | Module | Examples |
|-------|--------|----------|
| AML0001-AML0099 | General/Infrastructure | AML0001 Internal error, AML0002 Validation error, AML0003 Missing X-Request-ID, AML0004 Missing X-Device-Id |
| AML0100-AML0199 | Customer | AML0100 Not found, AML0101 Duplicate, AML0102 Invalid data, AML0103 KYC not verified, AML0104 KYC expired |
| AML0200-AML0299 | Account | AML0200 Not found, AML0201 Invalid data, AML0202 Suspended, AML0203 Inactive, AML0204 Insufficient balance |
| AML0300-AML0399 | Transaction | AML0300 Not found, AML0301 Invalid type, AML0302 Held for review, AML0303 Failed, AML0304 Invalid amount |
| AML0400-AML0499 | Alert | AML0400 Not found, AML0401 Creation failed |
| AML0500-AML0599 | Case | AML0500 Not found, AML0501 Already closed, AML0502 Invalid decision, AML0503 Not assigned, AML0504 Doc gen failed |
| AML0600-AML0699 | Rules Engine | AML0600 Rule execution failed, AML0601 Rule not found, AML0602 Threshold not configured |
| AML0700-AML0799 | Agent Orchestration | AML0700 Orchestration failed, AML0701 LLM API failed, AML0702 Agent timeout |
| AML0800-AML0899 | Simulation | AML0800 Scenario not found, AML0801 Simulation execution failed |
| AML0900-AML0999 | Authentication | AML0900 Auth required, AML0901 Insufficient permissions, AML0902 User not found, AML0903 User duplicate, AML0904 User inactive, AML0905 Invalid credentials |

### Standard API Headers (required on every request)
```
X-Request-ID: UUID      # Unique request identifier
X-Forwarded-For: String  # Customer IP address
X-Device-Id: String      # Device identifier
```

### Standard Error Response Format
```json
{
  "success": false,
  "error_code": "AML0100",
  "message": "Customer not found",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-07T10:00:00Z"
}
```

### Standard Success Response Format
```json
{
  "success": true,
  "data": { ... },
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-07T10:00:00Z"
}
```

### Middleware Flow
1. Extract `X-Request-ID` from header (or generate UUID if missing)
2. Extract `X-Forwarded-For` and `X-Device-Id`
3. Bind request_id to loguru context via `logger.bind(request_id=...)`
4. Log: `Incoming {method} {path} | IP: {ip} | Device: {device_id}`
5. Process request
6. Log: `Completed {method} {path} | Status: {status_code} | Duration: {ms}ms`

### Dependencies
Phase 1, Phase 2

---

## Phase 4: Module APIs (CRUD Controllers)

### What Gets Built
- Repository layer (database operations) for each module
- Service layer (business logic) for each module
- Controller/Router layer (API endpoints) for each module
- Pydantic schemas for request validation and response serialization

### Modules & Endpoints

**Customer Controller** (`/api/v1/customers`):
| Method | Path | Description |
|--------|------|-------------|
| POST | `/` | Create customer |
| GET | `/` | List customers (paginated) |
| GET | `/{customer_id}` | Get customer by ID |
| PUT | `/{customer_id}` | Update customer |

**Account Controller** (`/api/v1/accounts`):
| Method | Path | Description |
|--------|------|-------------|
| POST | `/` | Create account |
| GET | `/` | List accounts (paginated) |
| GET | `/{account_number}` | Get account by number |
| GET | `/customer/{customer_id}` | Get accounts by customer |
| PUT | `/{account_number}` | Update account |

**Transaction Controller** (`/api/v1/transactions`):
| Method | Path | Description |
|--------|------|-------------|
| POST | `/` | Create transaction (triggers AML rules synchronously) |
| GET | `/` | List transactions (paginated, filterable) |
| GET | `/{transaction_id}` | Get transaction by ID |
| GET | `/account/{account_number}` | Get transactions by account |

**Alert Controller** (`/api/v1/alerts`):
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List alerts (paginated, filterable) |
| GET | `/{alert_id}` | Get alert by ID |
| GET | `/account/{account_number}` | Get alerts by account |

**Case Controller** (`/api/v1/cases`):
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | List cases (paginated, filterable by status) |
| GET | `/{case_id}` | Get case with full details |
| GET | `/{case_id}/documents` | Get case document contents |
| POST | `/{case_id}/decisions` | Submit case decision (Accept/Reject) |
| POST | `/{case_id}/generate-sar` | Generate SAR document for case |

**User Controller** (`/api/v1/users`):
| Method | Path | Description |
|--------|------|-------------|
| POST | `/` | Create user |
| GET | `/` | List users (paginated) |
| GET | `/{user_id}` | Get user by ID |
| PUT | `/{user_id}` | Update user |

**Auth Controller** (`/api/v1/auth`):
| Method | Path | Description |
|--------|------|-------------|
| POST | `/login` | Authenticate user (bcrypt) and return bearer token |

### Architecture Pattern (per module)
```
Controller (router) → Service (logic) → Repository (DB)
     ↓                    ↓                   ↓
  Schemas            Exceptions            Models
```

### Files to Create
- `backend/app/schemas/auth.py`, `user.py`, `customer.py`, `account.py`, `transaction.py`, `alert.py`, `case.py`
- `backend/app/repositories/auth_repository.py`, `user_repository.py`, `customer_repository.py`, `account_repository.py`, `transaction_repository.py`, `alert_repository.py`, `case_repository.py`, `high_risk_account_repository.py`
- `backend/app/services/auth_service.py`, `user_service.py`, `customer_service.py`, `account_service.py`, `transaction_service.py`, `alert_service.py`, `case_service.py`
- `backend/app/controllers/auth_controller.py`, `user_controller.py`, `customer_controller.py`, `account_controller.py`, `transaction_controller.py`, `alert_controller.py`, `case_controller.py`

### Key Design Decisions
- Controllers only handle HTTP concerns (request parsing, response formatting)
- Services contain all business logic and orchestrate repositories
- Repositories are thin DB access wrappers (no business logic)
- All controllers receive standard headers via FastAPI `Depends()`
- Transaction POST endpoint triggers AML rules synchronously before returning

### Dependencies
Phase 1, Phase 2, Phase 3

---

## Phase 5: AML Rules Engine

### What Gets Built
- Abstract base rule class
- 6 concrete AML detection rules
- Rule engine orchestrator that runs all rules synchronously on each transaction
- High risk account flagging
- Alert generation

### AML Rules

| Rule ID | Name | Logic | Severity |
|---------|------|-------|----------|
| RULE-01 | High Deposit | `transaction_type == 'deposit' AND amount >= DEPOSIT_THRESHOLD` | high |
| RULE-02 | Negligible Profit Trade | Trade-sell where `profit <= NEGLIGIBLE_PROFIT_THRESHOLD` (compare with recent trade-buy on same account) | high |
| RULE-03 | Rapid Deposit-Withdrawal | Deposit followed by withdrawal within `RAPID_CYCLE_HOURS` on same account | medium |
| RULE-04 | Velocity Check | `>= VELOCITY_TXN_COUNT` transactions within `VELOCITY_WINDOW_MINUTES` on same account | medium |
| RULE-05 | Cross-Border Mismatch | `deposit_source_country != account holder's residency_country` | low |
| RULE-06 | High Risk Account | Account exists in `high_risk_accounts` table with `high_risk_flag = 1` | high |

### Base Rule Interface
```python
class BaseRule(ABC):
    rule_id: str
    rule_name: str

    @abstractmethod
    def evaluate(self, transaction, account, db) -> RuleResult:
        """Returns RuleResult(triggered=bool, severity=str, description=str)"""
```

### Rule Engine Flow
```
transaction_service.create_transaction()
    → Save transaction with status="pending"
    → Flag account as high risk (if not already) and insert into `high_risk_accounts` table 
    → rule_engine.evaluate_transaction(transaction, account, db)
        → For each rule in [RULE-01..RULE-06]:
            → rule.evaluate(transaction, account, db)
            → If triggered:
                → Create alert record
        → Return list of triggered alerts
    → If alerts exist:
        → Update transaction status to "held"
        → Trigger agent analysis (async background or inline)
    → If no alerts:
        → Update transaction status to "completed"
        → Update account balance
```

### Files to Create
- `backend/app/rules/__init__.py`
- `backend/app/rules/base_rule.py`
- `backend/app/rules/rule_engine.py`
- `backend/app/rules/high_deposit_rule.py`
- `backend/app/rules/negligible_profit_rule.py`
- `backend/app/rules/rapid_cycle_rule.py`
- `backend/app/rules/velocity_rule.py`
- `backend/app/rules/cross_border_rule.py`
- `backend/app/rules/high_risk_account_rule.py`

### Dependencies
Phase 1, Phase 2, Phase 3, Phase 4 (repositories for DB queries)

---

## Phase 6: AI Agent Orchestration (LangGraph)

### What Gets Built
- LangGraph state definition for agent pipeline
- Master Agent (AML Analyst) as LangGraph supervisor
- 5 analysis sub-agents (Behavioral, Network, Contextual, Evidence, False Positive)
- Document Content Generator sub-agent
- Agent tools for querying DB data
- Case creation from agent analysis results

### Agent Architecture (LangGraph StateGraph)

```
                    ┌─────────────────┐
                    │  Master Agent   │
                    │ (AML Analyst)   │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
     ┌──────▼──────┐  ┌─────▼─────┐  ┌──────▼──────┐
     │ Behavioral  │  │  Network  │  │ Contextual  │
     │  Analyst    │  │  Analyst  │  │   Scorer    │
     └──────┬──────┘  └─────┬─────┘  └──────┬──────┘
            │                │                │
            └────────────────┼────────────────┘
                             │
                    ┌────────▼────────┐
                    │    Evidence     │
                    │   Collector     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  False Positive │
                    │   Optimizer     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Document      │
                    │   Generator     │
                    └─────────────────┘
```

### LangGraph State Schema
```python
class AMLAnalysisState(TypedDict):
    alert_id: str
    account_number: str
    transaction_id: str

    # Data pulled for analysis
    customer_profile: dict
    account_info: dict
    transaction_history: list[dict]
    current_transaction: dict
    existing_alerts: list[dict]
    high_risk_info: dict | None

    # Sub-agent outputs
    behavioral_score: float
    behavioral_summary: str
    network_score: float
    network_summary: str
    contextual_score: float
    contextual_summary: str
    evidence_score: float
    evidence_summary: str
    false_positive_score: float
    false_positive_summary: str

    # Final outputs
    case_score_percentage: float
    case_classification: str  # false_positive / low / medium / high
    case_summary: str
    document_content: str
```

### Sub-Agent Responsibilities

| Agent | Input | Output | What It Does |
|-------|-------|--------|--------------|
| **Behavioral Analyst** | Customer profile, transaction history, current txn | score (0-100), summary | Analyzes if current behavior deviates from customer's historical pattern |
| **Network Analyst** | Account info, IP/device data, related accounts | score (0-100), summary | Identifies shared IPs, devices, cards suggesting coordinated activity |
| **Contextual Scorer** | All available data, KYC, risk rating | score (0-100), summary | Holistic risk assessment considering customer context |
| **Evidence Collector** | Transaction timeline, alerts, account activity | score (0-100), summary | Builds evidence timeline and identifies key suspicious indicators |
| **False Positive Optimizer** | All agent scores, historical FP rates | score (0-100), summary | Adjusts scoring to reduce false positives based on patterns |
| **Document Generator** | All agent outputs, case summary | SAR document content | Generates regulator-ready SAR narrative |

### Case Score Calculation
```python
case_score = (
    behavioral_score * 0.25 +
    network_score * 0.20 +
    contextual_score * 0.20 +
    evidence_score * 0.20 +
    false_positive_score * 0.15  # This is an INVERSE score (high = less likely FP)
)

# Classification (from DatabaseModel.md):
# 0-20   → False Positive
# 20-50  → Positive-Low Confidence
# 50-75  → Positive-Medium Confidence
# 75-100 → Positive-High Confidence
```

### Files to Create
- `backend/app/agents/__init__.py`
- `backend/app/agents/state.py` - AMLAnalysisState TypedDict
- `backend/app/agents/tools.py` - Agent tools for DB queries
- `backend/app/agents/master_agent.py` - LangGraph graph definition + supervisor
- `backend/app/agents/behavioral_analyst.py`
- `backend/app/agents/network_analyst.py`
- `backend/app/agents/contextual_scorer.py`
- `backend/app/agents/evidence_collector.py`
- `backend/app/agents/false_positive_optimizer.py`
- `backend/app/agents/document_generator.py`

### Key Design Decisions
- Behavioral, Network, and Contextual agents run in parallel (independent analysis)
- Evidence Collector runs after the first 3 (can reference their findings)
- False Positive Optimizer runs after Evidence Collector (needs all scores)
- Document Generator runs last (needs complete case data)
- Each agent gets a specialized system prompt with its role and analysis framework
- Agent tools provide read-only DB access (transaction history, customer data, etc.)
- LLM calls use structured output (Pydantic models) for reliable score+summary extraction

### Dependencies
Phase 1, Phase 2, Phase 3, Phase 4, Phase 5 (alerts to analyze)

---

## Phase 7: Case Management & SAR Generation

### What Gets Built
- Case creation from agent analysis output
- Case assignment to compliance managers
- Decision workflow (Accept/Reject)
- SAR document generation endpoint
- Transaction release/hold management based on decisions

### Decision Workflow
```
Case Created (status=OPEN, assigned_to=compliance_manager)
    │
    ▼
Compliance Manager reviews case details + agent analysis + documents
    │
    ├── ACCEPT → Case stays OPEN, transaction remains HELD
    │            next_action: "escalate" / "request-additional-documents" / "file-sar"
    │
    └── REJECT → Case status → CLOSE
                 Held transactions → status "completed"
                 Account balance updated
```

### SAR Generation
- POST `/api/v1/cases/{case_id}/generate-sar`
- Calls Document Content Generator agent with full case context
- Saves generated SAR content to `case_document_contents` table
- Returns the generated document content

### Key Design Decisions
- SAR generation can be triggered multiple times (versioned documents)
- When a case is REJECTED (false positive), held transactions are released

### Dependencies
Phase 1-6

---

## Phase 8: Transaction Simulation API

### What Gets Built
- Simulation controller and service
- Pre-defined simulation scenarios
- Manual transaction submission through same API

### Simulation Endpoints

**Simulation Controller** (`/api/v1/simulate`):
| Method | Path | Description |
|--------|------|-------------|
| POST | `/scenario` | Run a predefined simulation scenario |
| GET | `/scenarios` | List available simulation scenarios |

### Predefined Scenarios

| Scenario ID | Name | What It Does |
|-------------|------|--------------|
| `high_deposit` | High Amount Deposit | Creates a deposit of $50,000 (above DEPOSIT_THRESHOLD) |
| `negligible_profit` | Negligible Profit Trade | Deposit $500 → trade-buy $500 → trade-sell $500.01 |
| `rapid_cycle` | Rapid Deposit-Withdrawal | Deposit $5,000 → Withdrawal $4,950 within minutes |
| `velocity_burst` | Transaction Velocity Burst | 6 rapid small deposits in 30 minutes |
| `cross_border` | Cross-Border Deposit | Deposit from country different than customer's residency |
| `clean_transaction` | Normal Transaction | Legitimate $200 deposit (should NOT trigger alerts) |

### Key Design Decisions
- Simulation reuses the same `POST /api/v1/transactions` endpoint internally
- Scenarios are defined as data (not code) for easy addition
- Each scenario creates realistic transaction data with proper timestamps
- The simulation service calls `transaction_service.create_transaction()` which triggers the full AML pipeline

### Files to Create
- `backend/app/schemas/simulation.py`
- `backend/app/services/simulation_service.py`
- `backend/app/controllers/simulation_controller.py`

### Dependencies
Phase 1-5 (needs working transaction pipeline with rules)

---

## Phase 9: Seed Data & Testing

### What Gets Built
- Seed data for Organizations, Users, Customers, Accounts, Transactions
- Test fixtures and configuration
- Unit tests for rules engine
- Integration tests for full pipeline

### Seed Data

**Organizations**: 1 organization (ORG-0001, "Regulus Financial")
**Users**: 2 users
- USR-0001: admin (type=admin)
- USR-0002: compliance_manager1 (type=compliance_manager)

**Customers**: 3-5 sample customers with varying risk profiles
**Accounts**: 1 account per customer
**Transactions**: 10-20 transactions per account

### Test Strategy
- `conftest.py`: Test DB (separate SQLite), fixtures, standard headers
- Unit tests: Each rule tested in isolation with mock data
- Integration tests: Full flow from transaction → rules → alert → agent → case → decision
- Agent tests: Mock LLM responses to test pipeline without real API calls

### Files to Create
- `backend/seeds/seed_runner.py`
- `backend/seeds/seed_organizations.py`
- `backend/seeds/seed_users.py`
- `backend/seeds/seed_customers.py`
- `backend/seeds/seed_accounts.py`
- `backend/tests/conftest.py`
- `backend/tests/test_customers.py`
- `backend/tests/test_transactions.py`
- `backend/tests/test_rules_engine.py`
- `backend/tests/test_agents.py`
- `backend/tests/test_integration/test_end_to_end.py`

### Dependencies
All previous phases

---

## Phase Dependency Graph

```
Phase 1: Project Setup
    │
Phase 2: Database Layer
    │
Phase 3: Core API Framework
    │
Phase 4: Module APIs (CRUD)
   / \
  /   \
Phase 5: AML Rules Engine    Phase 8: Transaction Simulation
  │                                │
Phase 6: AI Agent Orchestration ───┘
  │
Phase 7: Case Management & SAR
  │
Phase 9: Seed Data & Testing
```

Phases 5 and 8 can be developed in parallel after Phase 4. Phase 6 depends on Phase 5. Phase 7 depends on Phase 6. Phase 9 is the final validation layer.

---

## Functional Flow Summary

```
[Transaction Created (manual or simulation)]
         │
         ▼
[Transaction Service: create_transaction()]
         │
         ▼
[Validate account exists and is active]
         │
         ▼
[Save transaction record (status=pending)]
         │
         ▼
[Check if account is in High Risk Accounts table]
         │──── YES → Create alert for existing high risk
         │
         ▼
[Rules Engine: evaluate all 6 rules synchronously]
         │
    ┌────┴────┐
    │         │
  TRIGGERED  NOT TRIGGERED
    │         │
    ▼         ▼
[Flag high   [Complete transaction]
 risk acct,  [Update account balance]
 Create      [Return success]
 alerts,
 Hold txn]
    │
    ▼
[For each alert → invoke Master Agent (LangGraph)]
    │
    ▼
[Master Agent delegates to 5 analysis sub-agents]
    │
    ▼
[Each sub-agent returns: score (0-100) + summary]
    │
    ▼
[Compute weighted case_score_percentage]
    │
    ▼
[Classify: FP (<20) | Low (20-50) | Med (50-75) | High (75-100)]
    │
    ▼
[Create Case record with all agent scores/summaries]
    │
    ▼
[Document Content Generator → save SAR draft to case_document_contents]
    │
    ▼
[Compliance Manager reviews case via API]
    │
    ▼
[Decision: ACCEPT or REJECT]
    │
    ├── ACCEPT → Transaction stays held, case remains open
    └── REJECT → Release held transactions, close case
    │
    ▼
[Decision saved to case_decisions table]
```

---

## Verification Plan

1. **Phase 1-3**: Run `uvicorn app.main:app --reload` and verify `/docs` shows Swagger UI, health endpoint returns 200, middleware logs request IDs
2. **Phase 4**: Use Swagger UI to CRUD customers, accounts; verify error codes for invalid requests
3. **Phase 5**: POST a transaction above threshold → verify alert created, transaction held
4. **Phase 6**: Verify agent pipeline creates case with scores/summaries (mock LLM for deterministic testing)
5. **Phase 7**: POST a decision on a case → verify case closes and held transactions release
6. **Phase 8**: POST `/api/v1/simulate/scenario` with `high_deposit` → verify full pipeline triggers
7. **Phase 9**: Run `python seeds/seed_runner.py` → verify data populated; run `pytest` → all pass
