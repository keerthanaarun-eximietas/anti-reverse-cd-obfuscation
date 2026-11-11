
from backend.data.seed_data import get_seed_transactions


# All application data lives in memory.
# Restarting Flask resets the data to its original sample state.

STATE = {
    "transactions": [],
    "audit_log": [],
}


def reset_store():
    """Restore the application to its initial sample state."""

    STATE["transactions"] = get_seed_transactions()
    STATE["audit_log"] = []

    return STATE


# Initialize the store when the application starts.
reset_store()
