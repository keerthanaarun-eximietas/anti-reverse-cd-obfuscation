
from datetime import datetime, timedelta


def get_seed_transactions():
    """Return a predictable set of synthetic transactions for testing."""

    now = datetime.now()

    return [
        {
            "id": "TXN-1001",
            "customer": "Customer A",
            "amount": 1200,
            "currency": "INR",
            "country": "IN",
            "account_country": "IN",
            "failed_attempts": 0,
            "account_age_days": 420,
            "created_at": (now - timedelta(minutes=15)).isoformat(),
        },
        {
            "id": "TXN-1002",
            "customer": "Customer B",
            "amount": 85000,
            "currency": "INR",
            "country": "IN",
            "account_country": "IN",
            "failed_attempts": 1,
            "account_age_days": 250,
            "created_at": (now - timedelta(minutes=12)).isoformat(),
        },
        {
            "id": "TXN-1003",
            "customer": "Customer C",
            "amount": 42000,
            "currency": "INR",
            "country": "US",
            "account_country": "IN",
            "failed_attempts": 2,
            "account_age_days": 90,
            "created_at": (now - timedelta(minutes=9)).isoformat(),
        },
        {
            "id": "TXN-1004",
            "customer": "Customer D",
            "amount": 150000,
            "currency": "INR",
            "country": "RU",
            "account_country": "IN",
            "failed_attempts": 5,
            "account_age_days": 2,
            "created_at": (now - timedelta(minutes=6)).isoformat(),
        },
        {
            "id": "TXN-1005",
            "customer": "Customer E",
            "amount": 750,
            "currency": "INR",
            "country": "IN",
            "account_country": "IN",
            "failed_attempts": 0,
            "account_age_days": 12,
            "created_at": (now - timedelta(minutes=3)).isoformat(),
        },
    ]
