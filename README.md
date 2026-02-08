# Regulus AML - AI-Powered Transaction Monitoring System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-orange.svg)](https://langchain-ai.github.io/langgraph/)
[![SQLite](https://img.shields.io/badge/SQLite-3.35+-yellow.svg)](https://www.sqlite.org)

An advanced AI-powered Anti-Money Laundering (AML) workflow automation system that detects suspicious financial transactions in real-time while dramatically reducing false positives through intelligent agent orchestration.

## 🚀 Features

### Core AML Capabilities

- **Real-time Transaction Monitoring**: Analyze transactions as they occur using configurable rule-based detection
- **AI-Powered Agent Orchestration**: Multi-agent system with specialized analysts for comprehensive investigation
- **Behavioral Analysis**: Machine learning models that learn normal customer patterns and detect deviations
- **Network Analysis**: Graph algorithms to identify coordinated fraud rings and suspicious connections
- **Contextual Risk Scoring**: Multi-factor risk assessment considering transaction history, behavior, and context
- **Automated Evidence Collection**: Intelligent gathering of relevant logs, transactions, and customer data
- **False Positive Reduction**: AI learning from analyst decisions to continuously improve detection accuracy

### Agent Architecture

- **AML Analyst (Master Agent)**: Orchestrates the investigation workflow
- **Behavioral Analyst**: Analyzes customer transaction patterns and behavioral deviations
- **Network Analyst**: Identifies suspicious network connections and coordinated activities
- **Contextual Scorer**: Evaluates risk based on transaction context and customer history
- **Evidence Collector**: Automatically gathers and organizes investigation evidence
- **False Positive Optimizer**: Reduces noise by learning from past decisions
- **Document Generator**: Creates regulator-ready Suspicious Activity Reports (SARs)

### Business Intelligence

- **Risk Classification**: Automatic categorization (False Positive, Low/Medium/High Confidence)
- **Case Management**: Complete workflow from alert to case resolution
- **SAR Generation**: Automated Suspicious Activity Report drafting
- **Compliance Workflow**: Structured review and approval process for compliance teams

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI API    │    │   SQLite DB     │
│   (React/Vue)   │◄──►│   Controllers    │◄──►│   Models        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Rule Engine    │
                       │   (6 Rules)      │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Agent Graph    │
                       │   (LangGraph)    │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Case Service   │
                       │   & Repository   │
                       └──────────────────┘
```

### AML Rules Engine

1. **High Deposit Rule**: Flags deposits above configurable threshold
2. **Negligible Profit Rule**: Detects trading with minimal profit/loss (potential laundering)
3. **Rapid Cycle Rule**: Identifies quick deposit-withdrawal cycles
4. **Velocity Rule**: Monitors transaction frequency bursts
5. **Cross-Border Rule**: Flags international transactions requiring review
6. **High Risk Account Rule**: Triggers alerts for accounts on watchlists

## 📋 Requirements

- Python 3.10 or higher
- SQLite 3.35 or higher
- API key for LLM provider (OpenAI or Google Gemini)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/RegulusOrgAI/regulus-aml-automation-agent.git
cd regulus-aml-automation-agent

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the `backend` directory:

```bash
# Database Configuration
DATABASE_URL=sqlite:///./regulus_aml.db

# AML Rule Thresholds
DEPOSIT_THRESHOLD=10000.0
NEGLIGIBLE_PROFIT_THRESHOLD=1.0
RAPID_CYCLE_HOURS=24
VELOCITY_TXN_COUNT=5
VELOCITY_WINDOW_MINUTES=60
CROSS_BORDER_ALERT_SEVERITY=high

# LLM Configuration (Choose one)
LLM_MODEL=gemini-2.5-flash
LLM_API_KEY=your-google-gemini-api-key

# OR for OpenAI
# LLM_MODEL=gpt-4o-mini
# LLM_API_KEY=your-openai-api-key

# Logging
LOG_LEVEL=DEBUG
```

### 3. Initialize Database

```bash
# Run the application to initialize database
uvicorn app.main:app --reload --port 8000
```

The application will automatically create the database schema on first run.

### 4. Seed Test Data

```bash
# Seed organizations, users, customers, accounts, and transactions
python -m seeds.seed_runner
```

### 5. Start the Application

```bash
# Development server
uvicorn app.main:app --reload --port 8000

# Production server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

### Base URL

```
http://localhost:8000/api/v1
```

### Required Headers

All API requests require these headers:

- `X-Request-ID`: Unique request identifier (UUID)
- `X-Forwarded-For`: Customer IP address
- `X-Device-ID`: Device identifier

### Endpoints

#### Customers

- `GET /customers` - List all customers
- `GET /customers/{customer_id}` - Get customer details
- `POST /customers` - Create new customer

#### Accounts

- `GET /accounts` - List all accounts
- `GET /accounts/{account_number}` - Get account details
- `POST /accounts` - Create new account

#### Transactions

- `GET /transactions` - List transactions
- `GET /transactions/{transaction_id}` - Get transaction details
- `POST /transactions` - Create new transaction (triggers AML analysis)

#### Alerts

- `GET /alerts` - List all alerts
- `GET /alerts/{alert_id}` - Get alert details
- `GET /alerts/account/{account_number}` - Get alerts for account

#### Cases

- `GET /cases` - List all cases
- `GET /cases/{case_id}` - Get case details
- `PUT /cases/{case_id}/decision` - Submit compliance decision

#### Simulation

- `GET /simulate/scenarios` - List available simulation scenarios
- `POST /simulate/{scenario_id}` - Run simulation scenario
- `POST /simulate/reset` - Reset all data (development only)

## 🎯 Usage Examples

### 1. Create a Customer

```bash
curl -X POST "http://localhost:8000/api/v1/customers" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: $(uuidgen)" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-123" \
  -d '{
    "customer_type": "individual",
    "full_name": "John Doe",
    "date_of_birth": "1985-06-15",
    "nationality": "US",
    "residency_country": "US",
    "id_type": "passport",
    "id_number": "P12345678",
    "phone": "+15551234567",
    "email": "john.doe@example.com",
    "address_line1": "123 Main St",
    "address_city": "New York",
    "address_country": "US",
    "kyc_status": "verified",
    "risk_rating": "medium"
  }'
```

### 2. Create an Account

```bash
curl -X POST "http://localhost:8000/api/v1/accounts" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: $(uuidgen)" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-123" \
  -d '{
    "customer_id": "CUST-000001",
    "account_type": "current",
    "account_status": "active",
    "branch_code": "NYC-001",
    "balance_amount": 5000.0,
    "balance_currency": "USD"
  }'
```

### 3. Create a Transaction (Triggers AML Analysis)

```bash
curl -X POST "http://localhost:8000/api/v1/transactions" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: $(uuidgen)" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-123" \
  -d '{
    "account_number": "ACC-100200300",
    "transaction_amount": 15000.0,
    "transaction_currency": "USD",
    "transaction_type": "deposit",
    "purpose": "Business payment",
    "deposit_source_type": "cardNumber",
    "deposit_source_value": "411111****1111",
    "deposit_source_country": "US"
  }'
```

### 4. Run Simulation Scenarios

```bash
# List available scenarios
curl -X GET "http://localhost:8000/api/v1/simulate/scenarios" \
  -H "X-Request-ID: $(uuidgen)" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-123"

# Run high deposit scenario
curl -X POST "http://localhost:8000/api/v1/simulate/high_deposit" \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: $(uuidgen)" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-123" \
  -d '{
    "account_number": "ACC-100200300"
  }'
```

### 5. Review Cases

```bash
# Get all cases
curl -X GET "http://localhost:8000/api/v1/cases" \
  -H "X-Request-ID: $(uuidgen)" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-123"

# Get case details (includes AI analysis results)
curl -X GET "http://localhost:8000/api/v1/cases/CASE-000001" \
  -H "X-Request-ID: $(uuidgen)" \
  -H "X-Forwarded-For: 192.168.1.100" \
  -H "X-Device-ID: device-123"
```

## 🧪 Testing

```bash
# Run unit tests
cd backend
pytest tests/

# Run integration tests
pytest tests/test_integration/

# Run specific test
pytest tests/test_customers.py -v
```

## 🔧 Configuration

### AML Rule Thresholds

Adjust these values in `.env` to tune detection sensitivity:

```bash
# High deposit threshold (default: $10,000)
DEPOSIT_THRESHOLD=10000.0

# Negligible profit threshold in USD (default: $1.0)
NEGLIGIBLE_PROFIT_THRESHOLD=1.0

# Rapid cycle detection window in hours (default: 24)
RAPID_CYCLE_HOURS=24

# Velocity detection: number of transactions (default: 5)
VELOCITY_TXN_COUNT=5

# Velocity detection: time window in minutes (default: 60)
VELOCITY_WINDOW_MINUTES=60
```

### LLM Configuration

Choose your AI provider:

**Google Gemini:**

```bash
LLM_MODEL=gemini-2.5-flash
LLM_API_KEY=your-gemini-api-key
```

**OpenAI:**

```bash
LLM_MODEL=gpt-4o-mini
LLM_API_KEY=your-openai-api-key
```

## 📊 Monitoring & Logging

### Log Format

All logs include structured information:

```
2026-02-07 15:30:45.123 | INFO     | req-12345 | app.main:42 | Starting AML analysis for alert ALERT-001
```

### Log Levels

- `DEBUG`: Detailed execution flow
- `INFO`: Normal operation events
- `WARNING`: Potential issues
- `ERROR`: System errors
- `CRITICAL`: Severe system issues

### Log Files

- Console output (development)
- `logs/regulus_aml.log` (production)

## 🚨 Error Codes

The system uses structured error codes for consistent error handling:

- **AML0001-AML0099**: General/Infrastructure errors
- **AML0100-AML0199**: Customer-related errors
- **AML0200-AML0299**: Account-related errors
- **AML0300-AML0399**: Transaction-related errors
- **AML0400-AML0499**: Alert-related errors
- **AML0500-AML0599**: Case-related errors
- **AML0600-AML0699**: Rules engine errors
- **AML0700-AML0799**: Agent orchestration errors
- **AML0800-AML0899**: Simulation errors
- **AML0900-AML0999**: Authentication errors

## 🏗️ Development

### Project Structure

```
backend/
├── app/
│   ├── agents/           # AI agent implementations
│   ├── controllers/      # API endpoints
│   ├── models/          # Database models
│   ├── repositories/    # Data access layer
│   ├── rules/           # AML rule implementations
│   ├── services/        # Business logic
│   ├── schemas/         # Pydantic models
│   └── config/          # Configuration
├── seeds/               # Test data
└── tests/               # Test suite
```

### Adding New AML Rules

1. Create rule class in `app/rules/`
2. Implement `evaluate()` method returning `RuleResult`
3. Add rule to `RuleEngine` in `app/rules/rule_engine.py`

### Adding New Agents

1. Create agent function in `app/agents/`
2. Implement agent logic using LLM
3. Add agent to graph in `app/agents/master_agent.py`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run linting and tests
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com) for high-performance APIs
- [LangGraph](https://langchain-ai.github.io/langgraph/) for agent orchestration
- [SQLAlchemy](https://www.sqlalchemy.org) for database management
- [Loguru](https://loguru.readthedocs.io) for structured logging

## 📞 Support

For questions, issues, or feature requests, please [open an issue](https://github.com/RegulusOrgAI/regulus-aml-automation-agent/issues) on GitHub.

---

**Regulus AML** - Turning 2,000 weekly alerts into 50 high-confidence cases with full investigation packs ready for review.
