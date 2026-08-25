from fastapi import FastAPI
from pydantic import BaseModel

from app.agents.customer_agent import agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Cohort 3 - Customer-Facing AI Agent",
    description="Track 1 - Build and Deploy a Customer-Facing AI Agent",
    version="0.3.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    content = final_message.content

    if isinstance(content, str):
        response_text = content
    elif isinstance(content, list):
        response_text = "\n".join(
            item.get("text", "")
            for item in content
            if isinstance(item, dict) and item.get("text")
        )
    else:
        response_text = str(content)

    return {
        "response": response_text
    }