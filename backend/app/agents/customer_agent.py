import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

load_dotenv()


class AgentState(TypedDict):
    customer_message: str
    response: str


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)


def customer_agent(state: AgentState):
    message = state["customer_message"]

    prompt = f"""
You are a professional banking customer support AI agent.

Help the customer clearly and safely.

Customer message:
{message}

Rules:
- Do not invent account or transaction information.
- Do not claim that a banking action has been completed unless a real tool confirms it.
- If information is missing, ask a concise clarification question.
- Be professional, empathetic, and concise.
"""

    result = llm.invoke(prompt)

    return {
        "response": result.content
    }


def build_agent():
    graph = StateGraph(AgentState)

    graph.add_node("customer_agent", customer_agent)

    graph.add_edge(START, "customer_agent")
    graph.add_edge("customer_agent", END)

    return graph.compile()


agent = build_agent()