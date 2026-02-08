from app.models.customer import Customer


def test_create_and_get_customer(client, standard_headers, db_session):
    payload = {
        "customer_type": "individual",
        "full_name": "Test User",
        "date_of_birth": "1990-01-01",
        "nationality": "US",
        "residency_country": "US",
        "id_type": "SSN",
        "id_number": "000-00-0000",
        "phone": "+1-555-0100",
        "email": "test@example.com",
        "address_line1": "1 Test St",
        "address_city": "Austin",
        "address_country": "US",
        "kyc_status": "verified",
        "kyc_verified_date": "2025-01-01",
        "kyc_expired_date": None,
        "risk_rating": "low",
    }

    create_resp = client.post("/api/v1/customers/", json=payload, headers=standard_headers)
    assert create_resp.status_code == 200
    customer_id = create_resp.json()["data"]["customer_id"]

    get_resp = client.get(f"/api/v1/customers/{customer_id}", headers=standard_headers)
    assert get_resp.status_code == 200
    assert get_resp.json()["data"]["customer_id"] == customer_id

    # Verify in DB
    assert db_session.query(Customer).filter(Customer.customer_id == customer_id).first() is not None
