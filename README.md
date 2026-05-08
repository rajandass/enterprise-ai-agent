# Enterprise AI Support Agent

Production-grade AI support platform built with FastAPI, OpenAI, ChromaDB, Azure App Service, Azure Application Insights, and enterprise security/observability practices.

---

# 🚀 Features

## AI & Retrieval

* Retrieval-Augmented Generation (RAG)
* OpenAI-powered question answering
* ChromaDB vector database
* Semantic document retrieval
* Automated ingestion pipeline

## API Platform

* FastAPI backend
* Swagger/OpenAPI documentation
* Structured API responses
* Request tracing
* Health probe endpoints

## Cloud & DevOps

* Azure App Service deployment
* GitHub Actions CI/CD pipeline
* Protected production deployments
* Branch protection rules
* Pull request governance

## Observability

* Azure Application Insights integration
* Structured logging
* Distributed tracing
* Live metrics monitoring
* Dependency tracking
* Production telemetry

## Security

* API key authentication
* Azure Key Vault integration
* Managed Identity authentication
* RBAC-based secret access
* Rate limiting protection

## Reliability & Operations

* Liveness probe
* Readiness probe
* Failed request alerting
* Availability alerting
* Latency alerting

---

# 🏗️ Architecture

```text
Client
   ↓
FastAPI API Layer
   ↓
Authentication & Rate Limiting
   ↓
RAG Pipeline
   ↓
OpenAI + ChromaDB
   ↓
Azure Monitoring & Telemetry
```

---

# 📂 Project Structure

```text
enterprise-ai-agent/
│
├── api/
│   └── main.py
│
├── pipelines/
│   ├── ingestion.py
│   └── query.py
│
├── data/
├── chroma_db/
├── .github/workflows/
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# ⚙️ Tech Stack

| Category      | Technology                 |
| ------------- | -------------------------- |
| Backend       | FastAPI                    |
| LLM           | OpenAI GPT                 |
| Vector DB     | ChromaDB                   |
| Cloud         | Azure App Service          |
| Observability | Azure Application Insights |
| Secrets       | Azure Key Vault            |
| Auth          | API Key Authentication     |
| CI/CD         | GitHub Actions             |
| Monitoring    | Azure Monitor              |
| Rate Limiting | SlowAPI                    |

---

# 🔐 Security Features

## API Authentication

All protected endpoints require:

```http
x-api-key: YOUR_API_KEY
```

---

## Key Vault Integration

Secrets are managed using:

* Azure Key Vault
* Managed Identity
* RBAC authorization

No production secrets are hardcoded.

---

## Rate Limiting

API requests are throttled using:

```text
5 requests per minute per client
```

Excess requests return:

```http
429 Too Many Requests
```

---

# 📊 Observability

## Application Insights

Integrated telemetry includes:

* Request tracing
* Dependency tracking
* Structured logs
* Performance monitoring
* Failure analytics

## Operational Alerts

Configured alerts:

* High failed requests
* Availability degradation
* High response latency

---

# ❤️ Health Probes

## Liveness Probe

```http
GET /health/live
```

Response:

```json
{
  "status": "alive"
}
```

---

## Readiness Probe

```http
GET /health/ready
```

Response:

```json
{
  "status": "ready",
  "checks": {
    "openai_api_key": true,
    "api_key": true
  }
}
```

---

# 🚀 Local Development

## 1. Clone Repository

```bash
git clone <repo-url>
cd enterprise-ai-agent
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

### Local Variables

```powershell
$env:OPENAI_API_KEY="your-openai-key"
$env:API_KEY="your-api-key"
$env:APPLICATIONINSIGHTS_CONNECTION_STRING="your-connection-string"
```

---

## 5. Run Application

```bash
uvicorn api.main:app --reload
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# ☁️ Azure Deployment

## Azure Services Used

* Azure App Service
* Azure Application Insights
* Azure Key Vault
* Azure Monitor

---

## CI/CD Pipeline

Deployment pipeline includes:

* GitHub Actions
* Pull request validation
* Protected main branch
* Manual production approvals

---

# 📈 Current Production Capabilities

✅ Enterprise Authentication
✅ Secret Management
✅ Production Monitoring
✅ Structured Logging
✅ Rate Limiting
✅ Health Monitoring
✅ Alerting
✅ CI/CD Governance
✅ Azure Deployment

---

# 🛣️ Planned Enhancements

* Redis caching
* Streaming responses
* Background job queues
* Async ingestion pipeline
* Frontend UI
* Kubernetes deployment
* Semantic caching
* Multi-tenant architecture

---

# 👨‍💻 Author

Rajan Dass

Enterprise AI Platform Engineering Project
