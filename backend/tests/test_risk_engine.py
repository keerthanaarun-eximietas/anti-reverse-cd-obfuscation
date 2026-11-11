
from backend.app.engines.risk_engine import calculate_risk


def make_transaction(**overrides):
    transaction = {
        "amount": 1000,
        "country": "IN",
        "account_country": "IN",
        "failed_attempts": 0,
        "account_age_days": 30,
    }
    transaction.update(overrides)
    return transaction


def test_low_risk_transaction_is_approved():
    result = calculate_risk(make_transaction())

    assert result["risk_score"] == 0
    assert result["risk_level"] == "LOW"
    assert result["decision"] == "APPROVE"


def test_high_amount_triggers_review():
    result = calculate_risk(make_transaction(amount=75000))

    assert result["risk_score"] == 30
    assert result["risk_level"] == "MEDIUM"
    assert result["decision"] == "REVIEW"


def test_foreign_transaction_adds_risk():
    result = calculate_risk(
        make_transaction(country="US")
    )

    assert result["risk_score"] == 25
    assert result["decision"] == "APPROVE"


def test_multiple_failed_attempts_add_risk():
    result = calculate_risk(
        make_transaction(failed_attempts=3)
    )

    assert result["risk_score"] == 20
    assert result["decision"] == "APPROVE"


def test_new_account_adds_risk():
    result = calculate_risk(
        make_transaction(account_age_days=2)
    )

    assert result["risk_score"] == 15
    assert result["decision"] == "APPROVE"


def test_combined_risk_conditions_cause_rejection():
    result = calculate_risk(
        make_transaction(
            amount=75000,
            country="US",
            failed_attempts=3,
            account_age_days=2,
        )
    )

    assert result["risk_score"] == 90
    assert result["risk_level"] == "HIGH"
    assert result["decision"] == "REJECT"


def test_risk_reasons_are_returned():
    result = calculate_risk(
        make_transaction(amount=75000, country="US")
    )

    assert "High transaction amount" in result["reasons"]
    assert "Transaction from a different country" in result["reasons"]
