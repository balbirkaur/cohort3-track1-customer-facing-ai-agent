from typing import TypedDict

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

from app.rag.knowledge_base import search_knowledge_base
from app.tools.transaction_tool import lookup_transaction


class AgentState(TypedDict):
    customer_message: str
    retrieved_context: str
    response: str


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)


def retrieve_policy(state: AgentState):
    results = search_knowledge_base(
        state["customer_message"],
        k=3,
    )

    context = "\n\n--- POLICY ---\n\n".join(results)

    return {
        "retrieved_context": context
    }


def generate_response(state: AgentState):
    prompt = f"""
You are a professional banking customer support AI agent.

Answer the customer's question using ONLY the banking
policy context provided below.

If the policy does not contain enough information:
- Do not invent an answer.
- Clearly say that additional verification is required.
- Recommend human support when appropriate.

Never request or expose:
- PIN
- Password
- OTP
- CVV
- Full card number

Customer message:
{state["customer_message"]}

Banking policy context:
{state["retrieved_context"]}

Provide a concise, professional and helpful response.
"""

    result = llm.invoke(prompt)

    return {
        "response": result.content
    }


def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("retrieve_policy", retrieve_policy)
    graph.add_node("generate_response", generate_response)

    graph.add_edge(START, "retrieve_policy")
    graph.add_edge("retrieve_policy", "generate_response")
    graph.add_edge("generate_response", END)

    return graph.compile()


agent = build_agent()