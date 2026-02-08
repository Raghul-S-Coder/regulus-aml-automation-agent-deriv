Module: Customer

1) Customers (flat + more fields)

{
  "customer_id": "CUST-000001",

  "customer_type": "individual",
  "full_name": "Vinoth Kumar",
  "date_of_birth": "1995-01-15",
  "nationality": "IN",
  "residency_country": "AE",
  "id_type": "passport",
  "id_number": "N1234567",
  "phone": "+971500000000",
  "email": "vinoth@example.com",
  "address_line1": "Business Bay",
  "address_city": "Dubai",
  "address_country": "AE",
  "kyc_status": "verified",
  "kyc_verified_date":"",
  "kyc_expired_date":"",
  "risk_rating": "medium",

  "created_date": "2026-02-07T10:00:00Z",
  "updated_date": "2026-02-07T10:00:00Z",
  "created_by": "system",
  "updated_by": "system"
}

2) Accounts (flat + more fields)

{
  "customer_id": "CUST-000001",
  "account_number": "ACC-100200300",

  "account_type": "current",
  "account_status": "active",
  "opened_date": "2024-06-01",
  "branch_code": "DXB-001",
  "balance_amount": 12500.75,
  "balance_currency": "AED",

  "created_date": "2026-02-07T10:00:00Z",
  "updated_date": "2026-02-07T10:00:00Z",
  "created_by": "system",
  "updated_by": "system"
}

3) High-risk accounts (flat + more fields)

{
  "account_number": "ACC-100200300",

  "high_risk_flag": 1, ( 0 - revoked, 1 - still risk)
  "overall_risk_score": 92,
  "risk_source": "watchlist" , negligible trade profit/loss, high amount deposit
  "risk_reason":"Matched watchlist record",
  "detected_date\":"2026-02-07T10:00:00Z"
  "created_date": "2026-02-07T10:00:00Z",
  "updated_date": "2026-02-07T10:00:00Z",
  "created_by": "system",
  "updated_by": "system"
}


⸻

Module: Transaction

1) Transactions (flat + more fields)

{
  "transaction_id": "TXN-0000001",
  "account_number": "ACC-100200300",

  "transaction_amount": 500.0,
  "transaction_currency": "AED",
  "transaction_date": "2026-02-07T10:00:00Z",
  "transaction_type": “deposit”, //(deposit, withdrawal, trade-buy and trade-sell),
  "transaction_status": "completed",
  "purpose": "Invoice #INV-1001",

  "deposit_source_type": "cardNumber",
  "deposit_source_value": "411111****1111",
  "deposit_source_country" : "AE"

  "created_date": "2026-02-07T10:00:00Z",
  "updated_date": "2026-02-07T10:00:00Z",
  "created_by": "system",
  "updated_by": "system"
}


⸻

Module: AML

1) AML Alerts (flat + more fields)

{
  "alert_id": "ALERT-000001",
  "account_number": "ACC-100200300",
  "alert_type": "transaction-monitoring",
  "severity": "high",
  "rule_id": "RULE-12",
  "description":"",
  "triggered_date": "2026-02-07T10:00:00Z",

  "created_date": "2026-02-07T10:00:00Z",
  "updated_date": "2026-02-07T10:05:00Z",
  "created_by": "aml-engine",
  "updated_by": "aml-engine"
}


⸻

Module: AML Analyst 

1) AML Cases (flat + more fields)

{
  "case_id": "CASE-000001",
  "alert_id": "ALERT-000001",
  "account_number": "ACC-100200300",
  "case_status": "OPEN", "CLOSE"
  "case_score_percentage": "" ( 0-20 False Positive, 20-50  Low Positive, 50-75 Medium Positive, 75-100 High Positive)
  "behavoir_agent_score" : "",
  "behavoir_agent_summary": "",
  "network_agent_score" : "",
  "network_agent_summary": "",
   "contextual_agent_score" : "",
  "contextual_agent_summary": "",
   "evidence_agent_score" : "",
  "evidence_agent_summary": "",
   "false_positive_agent_score" : "",
  "false_positive_agent_summary": "",
  "assigned_to": "compliance_user1",
  "assigned_date": "2026-02-07T10:06:00Z",
  "case_opened_date": "2026-02-07T10:06:00Z",
  "case_closed_date": null,
  "case_summary": "Investigate structuring pattern across multiple deposits."

  "created_date": "2026-02-07T10:06:00Z",
  "updated_date": "2026-02-07T10:06:00Z",
  "created_by": "analyst_1",
  "updated_by": "analyst_1"
}

2) Case decisions (flat + more fields)

{
  "case_id": "CASE-000001",

  "decision": "ACCEPT, REJECT",
  "decision_by": "compliance_user1",
  "decision_date": "2026-02-07T11:00:00Z",
  "decision_reason": "Pattern indicates possible structuring; needs compliance manager review.",
  "next_action": "request-additional-documents",

  "created_date": "2026-02-07T11:00:00Z",
  "updated_date": "2026-02-07T11:00:00Z",
  "created_by": "analyst_1",
  "updated_by": "analyst_1"
}