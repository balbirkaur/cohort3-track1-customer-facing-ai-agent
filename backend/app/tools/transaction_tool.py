from typing import Dict, Any


# Demo transaction data.
# Production version mein ye database/API se aayega.
TRANSACTIONS = {
    "TXN1001": {
        "transaction_id": "TXN1001",
        "status": "FAILED",
        "amount": 2500,
        "currency": "INR",
        "merchant": "ABC Store",
    },
    "TXN1002": {
        "transaction_id": "TXN1002",
        "status": "COMPLETED",
        "amount": 1200,
        "currency": "INR",
        "merchant": "XYZ Online",
    },
    "TXN1003": {
        "transaction_id": "TXN1003",
        "status": "PENDING",
        "amount": 3500,
        "currency": "INR",
        "merchant": "Demo Mart",
    },
}


def lookup_transaction(transaction_id: str) -> Dict[str, Any]:
    """
    Look up a transaction by transaction ID.
    """

    transaction = TRANSACTIONS.get(transaction_id)

    if not transaction:
        return {
            "found": False,
            "message": "Transaction not found.",
        }

    return {
        "found": True,
        "transaction": transaction,
    }