
from flask import Blueprint, jsonify, request

from backend.app.core.store import STATE
from backend.app.engines.risk_engine import calculate_risk


api = Blueprint("api", __name__, url_prefix="/api")


@api.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "message": "Transaction Risk API is running",
    })


@api.get("/transactions")
def get_transactions():
    transactions = []

    for item in STATE["transactions"]:
        transaction = dict(item)
        transaction.update(calculate_risk(transaction))
        transactions.append(transaction)

    return jsonify({
        "count": len(transactions),
        "transactions": transactions,
    })


@api.post("/transactions")
def create_transaction():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "A JSON request body is required"}), 400

    required_fields = [
        "customer",
        "amount",
        "currency",
        "country",
        "account_country",
        "failed_attempts",
        "account_age_days",
    ]

    missing_fields = [
        field for field in required_fields if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields,
        }), 400

    try:
        amount = float(data["amount"])
        failed_attempts = int(data["failed_attempts"])
        account_age_days = int(data["account_age_days"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "Amount, failed_attempts and account_age_days must be numeric",
        }), 400

    if amount <= 0 or failed_attempts < 0 or account_age_days < 0:
        return jsonify({
            "error": "Amount must be positive; attempt and account-age values cannot be negative",
        }), 400

    transaction = {
        "id": f"TXN-{1001 + len(STATE['transactions'])}",
        "customer": str(data["customer"]),
        "amount": amount,
        "currency": str(data["currency"]).upper(),
        "country": str(data["country"]).upper(),
        "account_country": str(data["account_country"]).upper(),
        "failed_attempts": failed_attempts,
        "account_age_days": account_age_days,
    }

    result = calculate_risk(transaction)
    transaction.update(result)

    STATE["transactions"].append(transaction)

    STATE["audit_log"].append({
        "transaction_id": transaction["id"],
        "action": "TRANSACTION_CREATED",
        "decision": result["decision"],
    })

    return jsonify({
        "message": "Transaction evaluated successfully",
        "transaction": transaction,
    }), 201


@api.get("/reports/summary")
def get_summary():
    transactions = STATE["transactions"]

    decisions = {
        "APPROVE": 0,
        "REVIEW": 0,
        "REJECT": 0,
    }

    for transaction in transactions:
        result = calculate_risk(transaction)
        decisions[result["decision"]] += 1

    return jsonify({
        "total_transactions": len(transactions),
        "decisions": decisions,
        "total_transaction_value": sum(
            transaction["amount"] for transaction in transactions
        ),
    })


@api.get("/audit")
def get_audit_log():
    return jsonify({
        "count": len(STATE["audit_log"]),
        "entries": STATE["audit_log"],
    })
