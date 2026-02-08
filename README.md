# Regulus AML - AI-Powered Transaction Monitoring System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green.svg)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.60-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.46-blue.svg)](https://www.sqlalchemy.org)
[![React](https://img.shields.io/badge/React-18.3.1-cyan.svg)](https://react.dev)

An advanced AI-powered Anti-Money Laundering (AML) workflow automation system that detects suspicious financial transactions in real-time while dramatically reducing false positives through intelligent agent orchestration and LangGraph-based multi-agent workflows.

## 🚀 Features

### Core AML Capabilities

- **Real-time Transaction Monitoring**: Analyze transactions as they occur using configurable rule-based detection
- **AI-Powered Agent Orchestration**: Multi-agent system with specialized LLM-powered analysts for comprehensive investigation
- **Behavioral Analysis**: LLM-based pattern analysis that evaluates if transactions deviate from normal customer behavior
- **Network Analysis**: Relationship analysis to identify coordinated activities and suspicious connections
- **Contextual Risk Scoring**: Multi-factor risk assessment considering transaction history, behavior, and customer context
- **Automated Evidence Collection**: Intelligent gathering and organization of relevant transaction data and indicators
- **False Positive Reduction**: LLM-assisted scoring optimization to reduce alert noise and focus on high-confidence cases

### Agent Architecture

- **AML Analyst (Master Agent)**: Orchestrates the investigation workflow
- **Behavioral Analyst**: Analyzes customer transaction patterns and behavioral deviations
- **Network Analyst**: Identifies suspicious network connections and coordinated activities
- **Contextual Scorer**: Evaluates risk based on transaction context and customer history
- **Evidence Collector**: Automatically gathers and organizes investigation evidence
- **False Positive Optimizer**: Analyzes all prior scores to estimate likelihood of false positives
- **Document Generator**: Creates regulator-ready Suspicious Activity Reports (SARs)

### Business Intelligence

- **Risk Classification**: Automatic categorization (False Positive, Low/Medium/High Confidence)
- **Case Management**: Complete workflow from alert to case resolution
- **SAR Generation**: Automated Suspicious Activity Report drafting
- **Compliance Workflow**: Structured review and approval process for compliance teams

## 🏗️ Architecture

```
┌─────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────┐
│   Frontend              │    │   FastAPI API Server     │    │   Database           │
│   (React + Tailwind)    │◄──►│   • Controllers          │◄──►│   (SQLAlchemy ORM)   │
│                         │    │   • Services             │    │                      │
└─────────────────────────┘    │   • Repositories         │    └──────────────────────┘
                               └──────────────────────────┘
                                        │
                                        ▼
                               ┌──────────────────────────┐
                               │   Rule Engine            │
                               │   • High Deposit Rule    │
                               │   • Negligible Profit    │
                               │   • Rapid Cycle          │
                               │   • Velocity Rule        │
                               │   • Cross-Border Rule    │
                               │   • High Risk Account     │
                               └──────────────────────────┘
                                        │
                                        ▼
                               ┌──────────────────────────┐
                               │   LangGraph Agent        │
                               │   • Master Agent         │
                               │   • Behavioral Analyst   │
                               │   • Network Analyst      │
                               │   • Contextual Scorer    │
                               │   • Evidence Collector   │
                               │   • False Positive Opt.  │
                               │   • Document Generator   │
                               └──────────────────────────┘
                                        │
                                        ▼
                               ┌──────────────────────────┐
                               │   AI-Powered Analysis    │
                               │   (LLM Integration)      │
                               └──────────────────────────┘
```

### AML Rules Engine (6 Rules)

1. **High Deposit Rule**: Flags transactions exceeding a configurable deposit threshold (default: $10,000) to detect structuring and large-value transactions requiring enhanced due diligence.

2. **Negligible Profit Rule**: Detects trading activity with minimal profit/loss margins (threshold: $1.0), indicating potential money laundering where funds are moved without genuine commercial intent.

3. **Rapid Cycle Rule**: Identifies rapid deposit-to-withdrawal cycles within a configurable time window (default: 24 hours) suggesting potential round-tripping or layering schemes.

4. **Velocity Rule**: Monitors transaction frequency bursts by flagging when transaction count exceeds a threshold (default: 5 transactions) within a specified time window (default: 60 minutes), detecting potential smurfing or structuring patterns.

5. **Cross-Border Rule**: Alerts on international transactions where the deposit source country differs from the customer's residency, requiring additional compliance review for high-risk jurisdictions.

6. **High Risk Account Rule**: Automatically triggers alerts for accounts flagged on internal watchlists or identified as high-risk based on customer KYC information and historical patterns.

## 📋 Requirements

- Python 3.11 or higher
- SQLAlchemy 2.0.46+ (PostgreSQL/SQLite compatible)
- API key for LLM provider (OpenAI GPT-4o-mini or Google Gemini 2.5-Flash)
- Node.js 18+ (for frontend)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/raghul-s-coder/regulus-aml-automation-agent-deriv.git
cd regulus-aml-automation-agent-deriv

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the `backend` directory:

```bash
# Database Configuration (SQLite or PostgreSQL)
DATABASE_URL=sqlite:///./regulus_aml.db
# DATABASE_URL=postgresql://user:password@localhost/regulus_aml  # For PostgreSQL

# LLM Provider Configuration
LLM_PROVIDER=gemini  # or 'openai'

# Google Gemini Configuration
GEMINI_MODEL=gemini-2.5-flash
GEMINI_API_KEY=your-google-gemini-api-key

# OpenAI Configuration (alternative)
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-openai-api-key

# AML Rule Thresholds
DEPOSIT_THRESHOLD=10000.0
NEGLIGIBLE_PROFIT_THRESHOLD=1.0
RAPID_CYCLE_HOURS=24
VELOCITY_TXN_COUNT=5
VELOCITY_WINDOW_MINUTES=60
CROSS_BORDER_ALERT_SEVERITY=high

# Logging
LOG_LEVEL=DEBUG

# CORS Origins (comma-separated)
FRONTEND_ORIGINS=http://localhost:5173,http://localhost:3000

# JWT Configuration
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=15
```

### 3. Install Frontend Dependencies

```bash
# Navigate to frontend directory
cd frontend
npm install
```

### 4. Initialize Database

```bash
# Run the application to initialize database
uvicorn app.main:app --reload --port 8000
```

The application will automatically create the database schema on first run.

### 5. Seed Test Data

```bash
# Seed organizations, users, customers, accounts, and transactions
python -m seeds.seed_runner
```

### 6. Start the Application

#### Backend Server

```bash
# Development server with auto-reload
cd backend
uvicorn app.main:app --reload --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with interactive documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

#### Frontend Application

```bash
# Development server
cd frontend
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

The frontend will be available at `http://localhost:5173` (Vite default)

### 7. Health Check

```bash
# Verify backend is running
curl http://localhost:8000/health
```

## 📖 API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Authentication

The system uses JWT token-based authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Standard Headers

All API requests should include these headers for proper request tracking and compliance:

- `X-Request-ID`: Unique request identifier (UUID v4) - **Required**
- `X-Forwarded-For`: Client IP address for audit logging - **Required**
- `X-Device-ID`: Client device identifier for enhanced security - **Required**

### Response Format

All API responses follow a consistent format:

```json
{
  "success": true,
  "data": {
    /* response data */
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-08T15:30:45.123Z"
}
```

**Paginated Response:**

```json
{
  "success": true,
  "data": {
    "items": [
      /* array of items */
    ],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-02-08T15:30:45.123Z"
}
```

### Endpoints

#### Authentication

- `POST /auth/login` - User login (returns JWT token)
- `POST /auth/refresh` - Refresh authentication token

#### Users

- `GET /users` - List all users with pagination
- `GET /users/{user_id}` - Get user details
- `POST /users` - Create new user
- `PUT /users/{user_id}` - Update user profile

#### Customers

- `GET /customers` - List all customers with pagination
- `GET /customers/{customer_id}` - Get customer KYC details
- `POST /customers` - Create new customer (onboarding)
- `PUT /customers/{customer_id}` - Update customer information

#### Accounts

- `GET /accounts` - List all accounts with pagination
- `GET /accounts/{account_number}` - Get account details
- `GET /accounts/customer/{customer_id}` - Get accounts by customer
- `POST /accounts` - Create new customer account
- `PUT /accounts/{account_number}` - Update account status/type

#### Transactions

- `GET /transactions` - List transactions with pagination and filters
- `GET /transactions/{transaction_id}` - Get transaction details
- `GET /transactions/account/{account_number}` - Get account transactions
- `POST /transactions` - Create new transaction (triggers AML analysis)

#### Alerts

- `GET /alerts` - List all alerts with pagination and filters
- `GET /alerts/{alert_id}` - Get alert details with rule violations
- `GET /alerts/account/{account_number}` - Get alerts for specific account

#### Cases

- `GET /cases` - List all cases with pagination and status filter
- `GET /cases/{case_id}` - Get case details with full AI analysis
- `GET /cases/{case_id}/documents` - Get case documents
- `POST /cases/{case_id}/decisions` - Submit compliance decision

#### Simulation (Development/Testing)

- `GET /simulate/scenarios` - List available test scenarios
- `POST /simulate/scenario` - Run a simulation scenario
- `POST /simulate/reset` - Reset all test data (development only)

## 🎯 Usage Examples

### 1. User Registration and Login

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "compliance_manager",
    "password": "SecurePassword123!"
  }'
# Returns: { "access_token": "eyJ...", "token_type": "bearer" }
```

### 2. Customer Onboarding (KYC)

```bash
curl -X POST "http://localhost:8000/api/v1/customers" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: 550e8400-e29b-41d4-a716-446655440000" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-mobile-123" \
  -d '{
    "customer_type": "individual",
    "full_name": "Jane Merchant",
    "date_of_birth": "1985-06-15",
    "nationality": "US",
    "residency_country": "US",
    "id_type": "passport",
    "id_number": "P12345678",
    "phone": "+15551234567",
    "email": "jane.merchant@example.com",
    "address_line1": "123 Main Street",
    "address_city": "New York",
    "address_country": "US",
    "kyc_status": "verified",
    "risk_rating": "medium"
  }'
```

### 3. Account Creation

```bash
curl -X POST "http://localhost:8000/api/v1/accounts" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: 550e8400-e29b-41d4-a716-446655440001" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-mobile-123" \
  -d '{
    "customer_id": "CUST-000001",
    "account_type": "checking",
    "account_status": "active",
    "branch_code": "NYC-001",
    "balance_amount": 5000.0,
    "balance_currency": "USD"
  }'
```

### 4. Transaction Creation (Triggers AML Analysis)

**When a transaction is created, the system automatically:**

1. Evaluates all 6 AML rules
2. Generates alerts for any rule violations
3. Creates a case with AI-powered investigation if alerts are generated
4. Invokes the LangGraph multi-agent workflow for comprehensive analysis

```bash
curl -X POST "http://localhost:8000/api/v1/transactions" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: 550e8400-e29b-41d4-a716-446655440002" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-mobile-123" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "account_number": "ACC-100200300",
    "transaction_amount": 15000.0,
    "transaction_currency": "USD",
    "transaction_type": "deposit",
    "transaction_date": "2026-02-08T10:30:00Z",
    "purpose": "Business invoice payment",
    "deposit_source_type": "bankTransfer",
    "deposit_source_value": "WIRE-123456789",
    "deposit_source_country": "US"
  }'
```

**Response includes:**

```json
{
  "success": true,
  "data": {
    "transaction_id": "TXN-000001",
    "status": "completed",
    "alerts_triggered": [
      {
        "alert_id": "ALERT-000001",
        "rule_violated": "HIGH_DEPOSIT",
        "severity": "high"
      }
    ],
    "case_created": {
      "case_id": "CASE-000001",
      "status": "under_investigation"
    }
  },
  "timestamp": "2026-02-08T10:30:45.123Z"
}
```

### 5. Review AI-Generated Case Analysis

```bash
# Get case details with AI analysis results
curl -X GET "http://localhost:8000/api/v1/cases/CASE-000001" \
  -H "X-Request-ID: 550e8400-e29b-41d4-a716-446655440003" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-mobile-123" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response includes comprehensive AI analysis:**

```json
{
  "success": true,
  "data": {
    "case_id": "CASE-000001",
    "status": "awaiting_decision",
    "alerts": [
      /* triggered alerts */
    ],
    "ai_analysis": {
      "behavioral_analysis": "Customer shows unusual deposit patterns...",
      "network_analysis": "No suspicious network connections detected...",
      "contextual_risk_score": 6.8,
      "evidence_collected": {
        /* transaction history, related accounts, etc */
      },
      "false_positive_assessment": "87% confidence this is legitimate business activity",
      "sar_document_draft": {
        /* SAR content ready for review */
      }
    },
    "recommended_action": "approve"
  },
  "timestamp": "2026-02-08T10:35:20.456Z"
}
```

### 6. Submit Compliance Decision

```bash
# Review and approve/reject case
curl -X PUT "http://localhost:8000/api/v1/cases/CASE-000001/decision" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: 550e8400-e29b-41d4-a716-446655440004" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-mobile-123" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "decision": "approve",
    "reason": "Verified business relationship with invoice documentation",
    "notes": "Customer provided supplier contract and invoice documentation"
  }'
```

### 7. Run Simulation Scenarios (for Testing)

```bash
# List available test scenarios
curl -X GET "http://localhost:8000/api/v1/simulate/scenarios" \
  -H "X-Request-ID: 550e8400-e29b-41d4-a716-446655440005" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-mobile-123" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Run high deposit simulation
curl -X POST "http://localhost:8000/api/v1/simulate/high_deposit" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: 550e8400-e29b-41d4-a716-446655440006" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-mobile-123" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "account_number": "ACC-100200300"
  }'
```

### 8. Export SAR Document

```bash
# Download generated SAR (Suspicious Activity Report) as PDF
curl -X GET "http://localhost:8000/api/v1/cases/CASE-000001/document" \
  -H "X-Request-ID: 550e8400-e29b-41d4-a716-446655440007" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-mobile-123" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -o case_sar_000001.pdf
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
cd backend
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_customers.py -v

# Run tests matching pattern
pytest -k "test_high_deposit" -v

# Run with coverage report
pytest --cov=app --cov-report=html

# Run integration tests
pytest tests/test_integration/ -v

# Run only AML rule tests
pytest tests/test_rules_engine.py -v
```

### Test Structure

```
backend/tests/
├── conftest.py                  # Pytest fixtures & configuration
├── test_agents.py               # Multi-agent workflow tests
├── test_customers.py            # Customer endpoint tests
├── test_rules_engine.py         # AML rules validation tests
├── test_transactions.py         # Transaction processing tests
└── test_integration/
    ├── test_end_to_end.py       # Full workflow tests
    └── test_alert_to_case.py    # Alert→Case lifecycle
```

### Example Test

```python
import pytest
from sqlalchemy.orm import Session
from app.models.customer import Customer
from app.services.customer_service import CustomerService
from app.schemas.customer import CustomerCreate

def test_create_customer(db_session: Session):
    """Test customer creation."""
    customer_data = CustomerCreate(
        customer_type="individual",
        full_name="Test Customer",
        date_of_birth="1990-01-15",
        nationality="US",
        residency_country="US",
        id_type="passport",
        id_number="ABC123456",
        phone="+15551234567",
        email="test@example.com",
        address_line1="123 Test St",
        address_city="New York",
        address_country="US",
        kyc_status="verified",
        risk_rating="low"
    )

    customer = CustomerService.create_customer(db_session, customer_data)

    assert customer.customer_id.startswith("CUST-")
    assert customer.full_name == "Test Customer"
    assert customer.kyc_status == "verified"
```

## 🔧 Configuration

### Environment Variables (`.env`)

#### Database

```bash
# SQLite (default)
DATABASE_URL=sqlite:///./regulus_aml.db

# PostgreSQL (production)
DATABASE_URL=postgresql://user:password@localhost:5432/regulus_aml
```

#### LLM Provider

```bash
# Use Google Gemini
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-api-key
GEMINI_MODEL=gemini-2.5-flash

# OR use OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4o-mini
```

#### AML Rule Thresholds

| Setting                       | Default | Description                                  |
| ----------------------------- | ------- | -------------------------------------------- |
| `DEPOSIT_THRESHOLD`           | 10000.0 | Transaction amount threshold (USD)           |
| `NEGLIGIBLE_PROFIT_THRESHOLD` | 1.0     | Minimum profit/loss for trading (USD)        |
| `RAPID_CYCLE_HOURS`           | 24      | Deposit-withdrawal cycle window (hours)      |
| `VELOCITY_TXN_COUNT`          | 5       | Transaction count threshold                  |
| `VELOCITY_WINDOW_MINUTES`     | 60      | Velocity detection window (minutes)          |
| `CROSS_BORDER_ALERT_SEVERITY` | high    | Alert severity for cross-border transactions |

#### Logging & Security

```bash
# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=DEBUG

# CORS origins (comma-separated)
FRONTEND_ORIGINS=http://localhost:5173,http://localhost:3000

# JWT Configuration
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=15
```

## 📊 Monitoring & Logging

### Structured Logging

The system uses **Loguru** for comprehensive structured logging with request context:

```python
# Log format includes:
# Timestamp | Level | Request ID | Module:Line | Message
2026-02-08 15:30:45.123 | INFO     | req-12345 | app.main:42 | Starting Regulus AML application
2026-02-08 15:30:46.456 | INFO     | req-12345 | app.rules.rule_engine:78 | Evaluating 6 AML rules for TXN-000001
2026-02-08 15:30:47.789 | WARNING  | req-12345 | app.agents.master_agent:156 | Alert generated: HIGH_DEPOSIT for TXN-000001
```

### Log Levels

| Level        | Purpose                 | Condition                                                    |
| ------------ | ----------------------- | ------------------------------------------------------------ |
| **DEBUG**    | Detailed execution flow | Development & troubleshooting                                |
| **INFO**     | Normal operation events | Application startup, rule evaluation, case creation          |
| **WARNING**  | Potential issues        | API rate limits, configuration issues, rule triggered        |
| **ERROR**    | System errors           | Database failures, API errors, validation failures           |
| **CRITICAL** | Severe issues           | Service unavailable, data corruption, authentication failure |

### Log Output

- **Console**: Real-time output during development (`uvicorn --reload`)
- **File**: Production logs in `logs/regulus_aml.log`

### Monitoring Metrics

The system tracks:

- **Performance**: Request latency, LLM response time, rule evaluation time
- **Quality**: Alert generation rate, false positive rate, case resolution time
- **Health**: Database connectivity, API availability, LLM service status

### Example Log Analysis

```bash
# View logs for specific transaction
grep "TXN-000001" logs/regulus_aml.log

# View all alerts generated
grep "Alert generated" logs/regulus_aml.log

# View error logs
grep "ERROR\|CRITICAL" logs/regulus_aml.log

# Monitor LLM performance
grep "LLM response time" logs/regulus_aml.log
```

## 🚨 Error Codes & Handling

The system uses structured error codes for consistent error handling and debugging:

| Code Range      | Category               | Examples                                      |
| --------------- | ---------------------- | --------------------------------------------- |
| AML0001-AML0099 | General/Infrastructure | Service initialization, database connection   |
| AML0100-AML0199 | Customer Management    | Customer not found, KYC verification failed   |
| AML0200-AML0299 | Account Management     | Account not found, insufficient balance       |
| AML0300-AML0399 | Transaction Processing | Invalid transaction, processing failed        |
| AML0400-AML0499 | Alert Generation       | Rule evaluation failed, alert creation error  |
| AML0500-AML0599 | Case Management        | Case not found, decision not allowed          |
| AML0600-AML0699 | Rules Engine           | Rule implementation error, evaluation failure |
| AML0700-AML0799 | Agent Orchestration    | Agent failure, LLM API error, graph execution |
| AML0800-AML0899 | Simulation             | Scenario not found, reset failed              |
| AML0900-AML0999 | Authentication         | Invalid credentials, token expired            |

### Example Error Response

```json
{
  "success": false,
  "error": {
    "code": "AML0100",
    "message": "Customer not found",
    "details": "Customer ID 'CUST-999999' does not exist in the system",
    "request_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "timestamp": "2026-02-08T10:30:45.123Z"
}
```

### Exception Handling

```python
# In your code
from app.exceptions import NotFoundException, ValidationException

try:
    customer = customer_service.get(customer_id)
except NotFoundException:
    # Handle not found - returns 404 with AML0100
    raise
except ValidationException as e:
    # Handle validation - returns 422 with specific error code
    raise
```

## 🏗️ Development

### Project Structure

```
backend/
├── app/
│   ├── agents/           # LangGraph multi-agent orchestration
│   │   ├── master_agent.py              # Master/Supervisor agent
│   │   ├── behavioral_analyst.py        # Pattern analysis
│   │   ├── network_analyst.py           # Network/graph analysis
│   │   ├── contextual_scorer.py         # Risk scoring
│   │   ├── evidence_collector.py        # Evidence gathering
│   │   ├── false_positive_optimizer.py  # ML-based noise reduction
│   │   ├── document_generator.py        # SAR generation
│   │   ├── state.py                     # Shared agent state
│   │   └── tools.py                     # Agent tools (DB access, etc)
│   │
│   ├── controllers/      # FastAPI routers & HTTP endpoints
│   │   ├── auth_controller.py
│   │   ├── customer_controller.py
│   │   ├── account_controller.py
│   │   ├── transaction_controller.py
│   │   ├── alert_controller.py
│   │   ├── case_controller.py
│   │   ├── user_controller.py
│   │   └── simulation_controller.py
│   │
│   ├── services/         # Business logic layer
│   │   ├── auth_service.py
│   │   ├── customer_service.py
│   │   ├── account_service.py
│   │   ├── transaction_service.py
│   │   ├── alert_service.py
│   │   ├── case_service.py
│   │   ├── user_service.py
│   │   ├── simulation_service.py
│   │   └── sar_pdf_generator.py
│   │
│   ├── repositories/     # Database access layer
│   │   ├── auth_repository.py
│   │   ├── customer_repository.py
│   │   ├── account_repository.py
│   │   ├── transaction_repository.py
│   │   ├── alert_repository.py
│   │   ├── case_repository.py
│   │   ├── user_repository.py
│   │   ├── organization_repository.py
│   │   └── high_risk_account_repository.py
│   │
│   ├── rules/            # AML rules engine
│   │   ├── base_rule.py              # Abstract rule class
│   │   ├── rule_engine.py            # Rules orchestrator
│   │   ├── high_deposit_rule.py      # RULE-01
│   │   ├── negligible_profit_rule.py # RULE-02
│   │   ├── rapid_cycle_rule.py       # RULE-03
│   │   ├── velocity_rule.py          # RULE-04
│   │   ├── cross_border_rule.py      # RULE-05
│   │   └── high_risk_account_rule.py # RULE-06
│   │
│   ├── models/           # SQLAlchemy ORM models
│   │   ├── organization.py
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── account.py
│   │   ├── transaction.py
│   │   ├── alert.py
│   │   ├── case.py
│   │   ├── case_document_content.py
│   │   ├── case_decision.py
│   │   └── high_risk_account.py
│   │
│   ├── schemas/          # Pydantic request/response schemas
│   │   ├── common.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── customer.py
│   │   ├── account.py
│   │   ├── transaction.py
│   │   ├── alert.py
│   │   ├── case.py
│   │   └── simulation.py
│   │
│   ├── config/
│   │   ├── settings.py               # Configuration management
│   │   ├── database.py               # SQLAlchemy setup
│   │
│   ├── exceptions/       # Error handling
│   │   ├── error_codes.py
│   │   ├── base_exception.py
│   │   └── handlers.py
│   │
│   ├── middleware/       # HTTP middleware
│   │   └── request_context.py        # Request tracking & context
│   │
│   └── utils/            # Utility functions
│       ├── id_generator.py           # ID generation (CUST-*, ACC-*, etc)
│       └── datetime_utils.py         # UTC timestamp helpers
│
├── seeds/                # Test data seeders
│   ├── seed_organizations.py
│   ├── seed_users.py
│   ├── seed_customers.py
│   ├── seed_accounts.py
│   ├── seed_transactions.py
│   └── seed_runner.py
│
├── tests/                # Unit & integration tests
│   ├── conftest.py
│   ├── test_agents.py
│   ├── test_customers.py
│   ├── test_rules_engine.py
│   ├── test_transactions.py
│   └── test_integration/
│
├── main.py
├── pyproject.toml        # Project metadata & dependencies
└── requirements.txt      # Python dependencies

frontend/
├── src/
│   ├── App.tsx           # Main React component
│   ├── main.tsx          # Entry point
│   ├── app/              # Application features
│   └── styles/           # Tailwind CSS
├── index.html
├── vite.config.ts        # Vite build configuration
├── tailwind.config.ts    # Tailwind configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Node.js dependencies
```

### Adding New AML Rules

To implement a custom AML rule:

1. **Create rule class** in `app/rules/`:

```python
from app.rules.base_rule import BaseRule, RuleResult

class MyCustomRule(BaseRule):
    """Rule description."""

    def __init__(self):
        super().__init__(
            rule_id="CUSTOM-001",
            rule_name="My Custom Rule",
            description="Detects specific suspicious pattern"
        )

    def evaluate(self, transaction, account, customer) -> RuleResult:
        """Evaluate rule logic."""
        if some_condition(transaction):
            return RuleResult(
                triggered=True,
                severity="high",
                reason="Explanation of why rule triggered"
            )
        return RuleResult(triggered=False)
```

2. **Register in RuleEngine** (`app/rules/rule_engine.py`):

```python
from app.rules.my_custom_rule import MyCustomRule

self.rules = [
    HighDepositRule(),
    # ... existing rules
    MyCustomRule(),  # Add here
]
```

3. **Test the rule**:

```bash
pytest tests/test_rules_engine.py -v -k "custom"
```

### Adding New AI Agents

To create a new specialized agent in the LangGraph workflow:

1. **Create agent module** in `app/agents/my_agent.py`:

```python
from app.agents.state import AMLAnalysisState

async def analyze(state: AMLAnalysisState, llm) -> dict:
    """Agent analysis function.

    Args:
        state: Current AML investigation state
        llm: Language model instance

    Returns:
        Updated state with agent's findings
    """
    # Extract context from state
    alert = state.get("alert")
    transaction = state.get("transaction")

    # Invoke LLM with context
    prompt = f"Analyze this alert: {alert}"
    response = await llm.ainvoke(prompt)

    # Update state with findings
    return {
        "my_agent_analysis": response.content,
        "my_agent_complete": True
    }
```

2. **Add to master agent graph** (`app/agents/master_agent.py`):

```python
from app.agents.my_agent import analyze as my_analyze

# In _build_graph():
graph.add_node("my_agent", lambda state: my_analyze(state, self.llm))
graph.add_edge("evidence_collector", "my_agent")
graph.add_edge("my_agent", "document_generator")
```

3. **Test the agent**:

```bash
pytest tests/test_agents.py -v -k "my_agent"
```

### Frontend Component Structure

Frontend uses **React 18** with **TypeScript** and **Tailwind CSS**:

```
frontend/src/
├── app/
│   ├── dashboard/        # Main dashboard
│   ├── alerts/          # Alert management UI
│   ├── cases/           # Case review interface
│   ├── customers/       # Customer management
│   ├── transactions/    # Transaction view
│   └── settings/        # Configuration UI
├── components/          # Reusable components
├── hooks/              # React custom hooks
├── services/           # API client functions
├── styles/             # Global styles
└── types/              # TypeScript types
```

## 🤝 Contributing

We welcome contributions! Here's the process:

1. **Fork the repository**

   ```bash
   git clone https://github.com/raghul-s-coder/regulus-aml-automation-agent-deriv.git
   cd regulus-aml-automation-agent
   ```

2. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 style guide (enforced by Ruff)
   - Add type hints to all functions
   - Write docstrings for classes and public methods

4. **Add tests for new functionality**

   ```bash
   # Your changes should include tests
   pytest tests/ -v --cov=app
   ```

5. **Run linting and formatting**

   ```bash
   cd backend
   ruff check --fix app/
   ruff format app/
   ```

6. **Commit with descriptive messages**

   ```bash
   git commit -m "feat: add new AML rule for smurfing detection

   - Implements detection for multiple small deposits
   - Adds configuration for deposit patterns
   - Includes comprehensive test coverage"
   ```

7. **Push and create a Pull Request**

   ```bash
   git push origin feature/your-feature-name
   ```

   - Reference any related issues (#123)
   - Describe changes and testing done
   - Ensure all CI checks pass

### Code Style

- **Python**: PEP 8 (Ruff enforced)
- **TypeScript**: ESLint + Prettier
- **Naming**: snake_case (Python), camelCase (TypeScript)
- **Comments**: Clear docstrings, not obvious comments

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Test addition/modification
- `refactor:` Code refactoring
- `perf:` Performance improvement
- `ci:` CI/CD changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[FastAPI](https://fastapi.tiangolo.com)** - High-performance Python web framework for building APIs
- **[LangGraph](https://langchain-ai.github.io/langgraph/)** - Multi-agent orchestration and workflow automation
- **[SQLAlchemy](https://www.sqlalchemy.org)** - Python SQL toolkit and Object Relational Mapper
- **[Loguru](https://loguru.readthedocs.io)** - Structured logging with context preservation
- **[Pydantic](https://docs.pydantic.dev)** - Data validation using Python type annotations
- **[React](https://react.dev)** - Frontend UI library for building interactive dashboards
- **[Tailwind CSS](https://tailwindcss.com)** - Utility-first CSS framework
- **[Vite](https://vitejs.dev)** - Next generation frontend tooling
- **[pytest](https://pytest.org)** - Testing framework for Python

## 📞 Support

For questions, issues, or feature requests:

### Create an Issue

Visit the [GitHub Issues](https://github.com/raghul-s-coder/regulus-aml-automation-agent-deriv/issues) page to:

- Report bugs with reproduction steps
- Request new features with use cases
- Ask questions about implementation

### Documentation

- **API Docs**: Available at `http://localhost:8000/docs` (Swagger UI)
- **Development**: See `ImplementationPlan.md` for architecture details
- **Database**: See `DatabaseModel.md` for schema documentation
- **Frontend**: See `FrontendImplementationPlan.md` for UI structure

### Support Resources

- Check existing issues for solutions
- Review documentation and error codes
- Run tests to validate your environment
- Enable DEBUG logging for troubleshooting

---

**Regulus AML** - Enterprise-grade transaction monitoring that transforms thousands of raw alerts into actionable, high-confidence cases with complete investigation documentation ready for regulatory review.

**Version**: 0.1.0 | **License**: MIT | **Status**: Active Development
