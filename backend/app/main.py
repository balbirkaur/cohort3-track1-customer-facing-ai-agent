from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.customer_agent import agent


app = FastAPI(
    title="Cohort 3 - Customer-Facing AI Agent",
    description="Track 1 - Build and Deploy a Customer-Facing AI Agent",
    version="0.3.0",
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    return {
        "message": "Customer-Facing AI Agent API is running",
        "track": "Cohort 3 - Track 1",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):
    result = agent.invoke(
        {
            "messages": [
                ("user", request.message)
            ]
        }
    )

    final_message = result["messages"][-1]

    return {
        "response": final_message.content
    }