from typing import Dict, Any

from langchain_core.tools import tool


@tool
def escalate_to_human(
    reason: str,
    priority: str = "high",
) -> Dict[str, Any]:
    """
    Escalate a customer issue to a human support representative.
    """

    return {
        "escalated": True,
        "priority": priority,
        "reason": reason,
        "status": "HUMAN_REVIEW_REQUIRED",
        "message": "The case has been escalated to human support.",
    }