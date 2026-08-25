from typing import Annotated, TypedDict

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_google_vertexai import ChatVertexAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from app.tools.transaction_tool import lookup_transaction
from app.tools.support_ticket_tool import create_support_ticket
from app.tools.escalation_tool import escalate_to_human
from app.rag.knowledge_base import search_knowledge_base


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


tools = [
    lookup_transaction,
    create_support_ticket,
    escalate_to_human,
]


llm = ChatVertexAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    project="cohort3-apac-505212",
    location="us-central1",
)

llm_with_tools = llm.bind_tools(tools)


SYSTEM_PROMPT = """
You are a professional banking customer support AI agent.

Your job is to help customers safely and accurately.

Available tools:

1. lookup_transaction
   Use when the customer provides a transaction ID or asks
   about a specific transaction.

2. create_support_ticket
   Use when:
   - the customer explicitly asks to create a support ticket, OR
   - the issue cannot be resolved using the available tools.

   If the customer has already described the issue, create the
   ticket immediately. Do not ask for additional details unless
   the issue is completely unclear.

3. escalate_to_human
   Use for suspected fraud, high-risk issues, or when the
   customer explicitly asks for a human representative.

Security rules:
- NEVER ask for PIN.
- NEVER ask for OTP.
- NEVER ask for password.
- NEVER ask for CVV.
- NEVER ask for the full card number.
- NEVER invent transaction information.
- NEVER claim an action was completed unless a tool confirms it.

For general banking policy questions, use the supplied
knowledge-base context.

If the knowledge base does not contain enough information,
say that additional verification is required.
"""


def call_model(state: AgentState):
    user_message = state["messages"][-1].content

    context = search_knowledge_base(
        user_message,
        k=3,
    )

    context_text = "\n\n--- POLICY ---\n\n".join(context)

    messages = [
        SystemMessage(
            content=SYSTEM_PROMPT
            + "\n\nBANKING KNOWLEDGE BASE:\n"
            + context_text
        )
    ]

    messages.extend(state["messages"])

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


def should_continue(state: AgentState):
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tools"

    return END


tool_node = ToolNode(tools)


def build_agent():
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END,
        },
    )

    workflow.add_edge("tools", "agent")

    return workflow.compile()


agent = build_agent()