
import pytest

from backend.app import create_app
from backend.app.core.store import reset_store


@pytest.fixture
def client():
    reset_store()

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client

    reset_store()


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_seed_transactions(client):
    response = client.get("/api/transactions")

    assert response.status_code == 200
    assert response.json["count"] == 5

    transactions = response.json["transactions"]

    assert len(transactions) == 5
    assert all("risk_score" in item for item in transactions)
    assert all("decision" in item for item in transactions)


def test_create_transaction(client):
    transaction = {
        "customer": "Test Customer",
        "amount": 75000,
        "currency": "INR",
        "country": "US",
        "account_country": "IN",
        "failed_attempts": 3,
        "account_age_days": 2,
    }

    response = client.post(
        "/api/transactions",
        json=transaction,
    )

    assert response.status_code == 201

    result = response.json["transaction"]

    assert result["risk_score"] == 90
    assert result["decision"] == "REJECT"
    assert result["risk_level"] == "HIGH"


def test_transaction_is_added_to_list(client):
    transaction = {
        "customer": "Another Customer",
        "amount": 1000,
        "currency": "INR",
        "country": "IN",
        "account_country": "IN",
        "failed_attempts": 0,
        "account_age_days": 30,
    }

    client.post("/api/transactions", json=transaction)

    response = client.get("/api/transactions")

    assert response.json["count"] == 6


def test_missing_fields_are_rejected(client):
    response = client.post(
        "/api/transactions",
        json={"customer": "Incomplete Customer"},
    )

    assert response.status_code == 400
    assert "fields" in response.json


def test_invalid_numeric_values_are_rejected(client):
    transaction = {
        "customer": "Invalid Customer",
        "amount": "not-a-number",
        "currency": "INR",
        "country": "IN",
        "account_country": "IN",
        "failed_attempts": 0,
        "account_age_days": 30,
    }

    response = client.post(
        "/api/transactions",
        json=transaction,
    )

    assert response.status_code == 400


def test_summary_endpoint(client):
    response = client.get("/api/reports/summary")

    assert response.status_code == 200

    summary = response.json

    assert summary["total_transactions"] == 5
    assert summary["decisions"]["APPROVE"] == 3
    assert summary["decisions"]["REVIEW"] == 1
    assert summary["decisions"]["REJECT"] == 1


def test_audit_log_records_new_transaction(client):
    transaction = {
        "customer": "Audit Customer",
        "amount": 1000,
        "currency": "INR",
        "country": "IN",
        "account_country": "IN",
        "failed_attempts": 0,
        "account_age_days": 30,
    }

    client.post("/api/transactions", json=transaction)

    response = client.get("/api/audit")

    assert response.status_code == 200
    assert response.json["count"] == 1
    assert response.json["entries"][0]["action"] == "TRANSACTION_CREATED"
