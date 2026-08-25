from typing import Dict, Any

from langchain_core.tools import tool


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


@tool
def lookup_transaction(transaction_id: str) -> Dict[str, Any]:
    """
    Look up a banking transaction using its transaction ID.
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