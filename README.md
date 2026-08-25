# 🏦 BankAssist AI — Customer Resolution Agent

### APAC GenAI Academy · Cohort 3 · Track 1

An AI-powered banking customer support agent that combines **Google Cloud Vertex AI, Gemini, LangGraph, RAG, and tool calling** to resolve customer issues safely and accurately.

🔗 **Live Demo:**  
https://cohort3-customer-agent-web-215731609750.us-central1.run.app

---

## 🚀 Overview

BankAssist AI is an intelligent banking customer-support agent designed to:

- Answer banking policy questions
- Search a banking knowledge base using RAG
- Look up transaction details
- Create support tickets
- Escalate high-risk or fraud-related issues to a human
- Follow banking security rules
- Avoid requesting sensitive credentials such as OTP, PIN, CVV, passwords, or full card numbers

The application uses a **LangGraph agent workflow** with Gemini running through **Google Cloud Vertex AI**.

---

# 🏗️ Architecture

```text
                         ┌─────────────────────────┐
                         │       Next.js UI        │
                         │     Customer Support    │
                         └────────────┬────────────┘
                                      │
                                      │ HTTPS / JSON
                                      ▼
                         ┌─────────────────────────┐
                         │      Cloud Run API      │
                         │       FastAPI            │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       LangGraph         │
                         │   Customer Agent        │
                         └────────────┬────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
             ┌────────────┐   ┌──────────────┐   ┌──────────────┐
             │ Gemini     │   │ RAG / FAISS  │   │ Agent Tools  │
             │ Vertex AI  │   │ Knowledge KB │   │              │
             └────────────┘   └──────────────┘   └──────┬───────┘
                                                        │
                                      ┌─────────────────┼────────────────┐
                                      │                 │                │
                                      ▼                 ▼                ▼
                              Transaction Lookup   Support Ticket   Human Escalation
```

---

# 🧠 AI Agent Workflow

```text
START
  │
  ▼
Agent Node
  │
  ├── General banking question
  │        ↓
  │      RAG Search
  │        ↓
  │      Gemini
  │
  ├── Transaction question
  │        ↓
  │   Transaction Tool
  │        ↓
  │      Gemini
  │
  ├── Support issue
  │        ↓
  │   Support Ticket Tool
  │
  └── Fraud / high-risk issue
           ↓
      Human Escalation
```

---

# ✨ Key Capabilities

## 1. 🔎 Knowledge Search

The agent answers banking policy questions using the supplied banking knowledge base.

Example:

```text
What should I do if my debit card is lost or stolen?
```

---

## 2. 💳 Transaction Lookup

Example:

```text
Please check transaction TXN1001.
```

Example response:

```text
The transaction TXN1001 with merchant ABC Store for 2500 INR has failed.
```

The agent does not invent transaction information.

---

## 3. 🎫 Support Tickets

The agent can create a support ticket when:

- The customer explicitly requests one
- The issue cannot be resolved with available tools

Example:

```text
I have a problem with my card payment. Please create a support ticket.
```

---

## 4. 🚨 Human Escalation

High-risk situations such as suspected fraud can be escalated.

Example:

```text
I don't recognize a transaction on my account. I think it may be fraud.
```

---

# 🔐 Security Rules

The agent is explicitly instructed never to request or expose:

- ❌ OTP
- ❌ PIN
- ❌ Password
- ❌ CVV
- ❌ Full card number

The system also follows these rules:

- Never invent transaction information
- Never claim an action was completed unless a tool confirms it
- Escalate high-risk/fraud situations
- Request additional verification when the knowledge base does not contain enough information

---

# 📚 RAG Implementation

The banking policy document is stored at:

```text
data/
└── knowledge-base/
    └── banking_policies.txt
```

The RAG pipeline:

```text
Banking Policy Document
        │
        ▼
RecursiveCharacterTextSplitter
        │
        ├── chunk_size = 800
        └── chunk_overlap = 100
        │
        ▼
Google Vertex AI Embeddings
        │
        ▼
FAISS Vector Store
        │
        ▼
Similarity Search
        │
        ▼
Top-K Relevant Documents
        │
        ▼
Gemini Agent
```

The application retrieves the top 3 relevant chunks.

---

# 🤖 Google Vertex AI

The application uses Gemini through **Google Cloud Vertex AI** rather than depending on an AI Studio API key.

Configuration:

```text
GOOGLE_CLOUD_PROJECT=cohort3-apac-505212
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=TRUE
```

Cloud Run uses a Google Cloud service account for authentication.

---

# ☁️ Google Cloud Services

- Google Cloud Run
- Vertex AI
- Gemini
- Cloud Build
- Artifact Registry
- Cloud IAM

---

# 🐳 Containerization

The backend is deployed using a Dockerfile.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

COPY backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

COPY data ./data

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

The application is built from the project root so both `backend/` and `data/` are available inside the container.

---

# 📁 Project Structure

```text
cohort3-track1-customer-facing-ai-agent/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   └── customer_agent.py
│   │   ├── rag/
│   │   │   └── knowledge_base.py
│   │   ├── tools/
│   │   │   ├── transaction_tool.py
│   │   │   ├── support_ticket_tool.py
│   │   │   └── escalation_tool.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Procfile
│   └── runtime.txt
│
├── data/
│   └── knowledge-base/
│       └── banking_policies.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── .env.production
│   ├── Dockerfile
│   ├── package.json
│   └── next.config.ts
│
├── Dockerfile
├── .dockerignore
└── README.md
```

---

# 💻 Local Development

## Prerequisites

- Python 3.12
- Node.js
- npm
- Google Cloud CLI
- Google Cloud project with Vertex AI enabled

### Google Cloud Authentication

```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project cohort3-apac-505212
gcloud config set project cohort3-apac-505212
```

### Backend Setup

```bash
cd backend
python -m venv .venv
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### Vertex AI Environment — PowerShell

```powershell
$env:GOOGLE_CLOUD_PROJECT="cohort3-apac-505212"
$env:GOOGLE_CLOUD_LOCATION="us-central1"
$env:GOOGLE_GENAI_USE_VERTEXAI="TRUE"
```

### Start Backend

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 Local API Test

PowerShell:

```powershell
$body = @{
    message = "Please check transaction TXN1001."
} | ConvertTo-Json -Compress

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/chat" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body

$response
```

Expected:

```text
The transaction TXN1001 with merchant ABC Store for 2500 INR has failed.
```

---

# ☁️ Cloud Run Deployment

The backend is deployed from the **project root**.

```bash
gcloud run deploy cohort3-customer-agent-api \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --service-account 215731609750-compute@developer.gserviceaccount.com \
  --clear-base-image \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=cohort3-apac-505212,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=TRUE"
```

The root-level Dockerfile ensures that the knowledge base is included:

```text
/app/data/knowledge-base/banking_policies.txt
```

---

# 🌍 Production URLs

### Frontend

https://cohort3-customer-agent-web-215731609750.us-central1.run.app

### Backend

https://cohort3-customer-agent-api-215731609750.us-central1.run.app

### Backend Swagger

https://cohort3-customer-agent-api-215731609750.us-central1.run.app/docs

---

# 🎨 Frontend

The frontend is a Next.js application.

Production API URL:

```env
NEXT_PUBLIC_API_URL=https://cohort3-customer-agent-api-215731609750.us-central1.run.app
```

File:

```text
frontend/.env.production
```

Because `NEXT_PUBLIC_*` variables are embedded during the Next.js build, the frontend must be rebuilt/redeployed whenever this value changes.

---

# 🚀 Frontend Deployment

```bash
gcloud run deploy cohort3-customer-agent-web \
  --source frontend \
  --region us-central1 \
  --allow-unauthenticated
```

---

# 🧪 Test Scenarios

### Test 1 — Transaction Lookup

```text
Please check transaction TXN1001.
```

Expected:

```text
TXN1001
ABC Store
2500 INR
Failed
```

### Test 2 — Banking Policy

```text
What should I do if my debit card is lost or stolen?
```

Expected behavior:

```text
Search knowledge base
        ↓
Retrieve banking policy
        ↓
Gemini generates answer
```

### Test 3 — Support Ticket

```text
My card payment is not working. Please create a support ticket.
```

Expected behavior:

```text
Support ticket tool is invoked.
```

### Test 4 — Fraud

```text
I don't recognize a transaction on my account. I think it may be fraud.
```

Expected behavior:

```text
Human escalation tool
```

### Test 5 — Unknown Transaction

```text
Please check transaction TXN9999.
```

The agent must not invent transaction information.

### Test 6 — Sensitive Information

```text
What is my OTP for transaction TXN1001?
```

The agent must not provide or request OTP.

---

# 🔄 End-to-End Flow

```text
Customer
   │
   ▼
Next.js Frontend
   │
   │ HTTPS
   ▼
Cloud Run
FastAPI Backend
   │
   ▼
LangGraph
   │
   ▼
Customer Agent
   │
   ├───────────────┐
   │               │
   ▼               ▼
RAG             Gemini
FAISS           Vertex AI
   │               │
   └───────┬───────┘
           │
           ▼
       Tool Calling
           │
     ┌─────┼──────────────┐
     ▼     ▼              ▼
Transaction Ticket     Escalation
 Lookup    Creation       Human
     │     │              │
     └─────┴──────┬───────┘
                  ▼
             Final Response
                  │
                  ▼
               Customer
```

---

# 🛡️ Security Considerations

For production banking environments, additional controls should be implemented, including:

- Authentication
- Authorization
- Customer identity verification
- Audit logging
- Encryption
- Secrets management
- Rate limiting
- PII redaction
- Human approval for sensitive actions
- Transaction authorization controls

---

# 📌 Key Technical Highlights

### Frontend
- Next.js
- TypeScript
- React
- Responsive UI

### Backend
- Python
- FastAPI
- LangChain
- LangGraph

### AI
- Google Gemini
- Vertex AI
- Tool Calling
- RAG

### Retrieval
- Recursive Character Text Splitter
- Google embeddings
- FAISS
- Similarity Search

### Deployment
- Google Cloud Run
- Cloud Build
- Artifact Registry
- Docker
- Cloud IAM
- Vertex AI service-account authentication

---

# 🏆 Project Highlights

This project demonstrates an end-to-end **agentic AI customer support architecture**, rather than a simple chatbot.

- ✅ Agent orchestration with LangGraph
- ✅ Gemini tool calling
- ✅ RAG-based knowledge retrieval
- ✅ Transaction lookup
- ✅ Automated support ticket creation
- ✅ Human escalation
- ✅ Security-aware prompting
- ✅ Vertex AI integration
- ✅ Cloud Run deployment
- ✅ Docker-based production deployment
- ✅ Next.js frontend
- ✅ FastAPI backend
- ✅ Production CORS configuration

---

# 👩‍💻 Author

**Balbir Kaur**

APAC GenAI Academy  
Cohort 3 · Track 1

---

## ⭐ Project Status

**Production deployed and operational.**

Frontend: ✅  
Backend: ✅  
Vertex AI Gemini: ✅  
RAG + FAISS: ✅  
LangGraph Agent: ✅  
Transaction Lookup: ✅  
Cloud Run: ✅
