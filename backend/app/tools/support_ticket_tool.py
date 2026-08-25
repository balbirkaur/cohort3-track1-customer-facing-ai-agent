from typing import Dict, Any
from uuid import uuid4

from langchain_core.tools import tool


@tool
def create_support_ticket(
    customer_issue: str,
    priority: str = "medium",
) -> Dict[str, Any]:
    """
    Create a support ticket for issues requiring human assistance.
    """

    ticket_id = f"TKT-{uuid4().hex[:8].upper()}"

    return {
        "success": True,
        "ticket_id": ticket_id,
        "priority": priority,
        "status": "OPEN",
        "issue": customer_issue,
        "message": "Support ticket created successfully.",
    }