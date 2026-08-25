# 🏦 Banking Customer Resolution Agent

> **APAC GenAI Academy · Cohort 3 · Track 1**
>
> Build and Deploy a Customer-Facing AI Agent

An AI-powered banking customer support agent designed to resolve common customer issues using **Gemini, LangGraph, RAG, transaction tools, support-ticket creation, and human escalation**.

---

## 🚀 Live Demo

### Customer-Facing Application

🔗 **Live URL:**  
`<ADD_FRONTEND_CLOUD_RUN_URL>`

### Backend API

🔗 **Cloud Run API:**  
https://cohort3-customer-agent-api-215731609750.us-central1.run.app

### API Documentation

🔗 **Swagger / OpenAPI:**  
https://cohort3-customer-agent-api-215731609750.us-central1.run.app/docs

---

## 🎯 Project Objective

The Banking Customer Resolution Agent provides a customer-facing conversational interface that can:

- Answer banking policy questions using RAG
- Look up transaction information
- Handle failed or disputed payments
- Create customer support tickets
- Escalate fraud-related or sensitive cases to human support
- Provide grounded and actionable responses

The goal is to demonstrate an **agentic customer-support workflow** rather than a simple question-answering chatbot.

---

# 🧠 Key Capabilities

| Capability                 | Implementation        |
| -------------------------- | --------------------- |
| 💬 Customer Conversation   | Next.js               |
| 🤖 AI Agent                | Gemini                |
| 🔀 Agent Orchestration     | LangGraph             |
| 🔎 Knowledge Retrieval     | RAG + FAISS           |
| 💳 Transaction Lookup      | Tool                  |
| 🎫 Support Ticket Creation | Tool                  |
| 👤 Human Escalation        | Tool                  |
| 🔐 API Key Management      | Google Secret Manager |
| 🚀 Backend Deployment      | Google Cloud Run      |
| 🌐 Frontend Deployment     | Google Cloud Run      |
| 📦 Source Control          | GitHub                |

---

# 🏗️ Architecture

```text
                         CUSTOMER
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Next.js Frontend  │
                 │  Customer Chat UI   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    FastAPI API      │
                 │    /chat endpoint   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     LangGraph       │
                 │   Customer Agent    │
                 └──────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
       ┌────────────┐ ┌────────────┐ ┌──────────────┐
       │    RAG     │ │ Transaction│ │   Support    │
       │ Knowledge  │ │    Tool    │ │    Tools     │
       │   Base     │ │            │ │              │
       └─────┬──────┘ └────────────┘ └──────┬───────┘
             │                               │
             ▼                               ▼
       ┌────────────┐                ┌──────────────┐
       │    FAISS   │                │ Ticket /     │
       │ Vector     │                │ Escalation   │
       │  Search    │                │              │
       └────────────┘                └──────────────┘
              │
              └─────────────┬─────────────┘
                            ▼
                    ┌──────────────┐
                    │    Gemini    │
                    │     API      │
                    └──────────────┘
                            │
                            ▼
                     FINAL RESPONSE
```
