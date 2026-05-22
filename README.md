# Enterprise AI Agent Platform

Production-grade AI/RAG platform built with FastAPI, Azure cloud services, enterprise observability, and scalable deployment architecture.

---

# Overview

The Enterprise AI Agent Platform is an enterprise-focused AI backend system designed for:

* Retrieval-Augmented Generation (RAG)
* Intelligent tutoring systems
* Enterprise observability
* Production-grade deployment workflows
* Scalable AI infrastructure
* Azure-native integrations

The platform currently powers:

* NEET Biology AI tutoring workflows
* Semantic retrieval pipelines
* Persistent conversational memory
* Adaptive tutoring foundations
* Production-ready deployment pipelines

---

# Core Architecture

```text
Client Applications
        ↓
FastAPI Backend
        ↓
Middleware Layer
(Request Logging / Tracing / Rate Limiting)
        ↓
RAG & AI Services
        ↓
Azure OpenAI + Azure AI Search
        ↓
Persistence & Memory Layer
(Cosmos DB / Redis / Blob Storage)
        ↓
Observability & Monitoring
(Application Insights / Structured Logs)
```

---

# Technology Stack

## Backend

* FastAPI
* Python 3.10
* Uvicorn
* Pydantic

## AI & Retrieval

* Azure OpenAI
* Azure AI Search
* Vector Retrieval
* Semantic Chunk Search

## Cloud & Infrastructure

* Azure App Service
* Azure Container Registry (ACR)
* Azure Key Vault
* Managed Identity
* RBAC
* Azure Blob Storage
* Cosmos DB
* Redis

## Observability

* Azure Application Insights
* Structured Logging
* Request Tracing
* Dependency Health Monitoring

## DevOps

* GitHub Actions
* Docker
* CI/CD Pipelines
* Feature Branch Deployments

---

# Key Features

## Platform Foundation

* Layered FastAPI architecture
* Structured middleware pipeline
* Centralized configuration management
* Global exception handling
* Request correlation IDs

## Health & Readiness

* `/health/live` endpoint
* `/health/ready` endpoint
* Dependency-aware readiness validation
* Startup dependency validation
* Structured readiness logging

## AI/RAG Platform

* Embedding generation
* Azure AI Search vector retrieval
* Semantic chunk retrieval
* Tutor memory architecture
* Session persistence
* Adaptive tutoring foundations

## Security

* API key authentication
* Azure Key Vault secret references
* Managed Identity integration
* RBAC-based access control
* Centralized secret management

## Observability

* Structured logging
* Request tracing
* Startup audit logging
* Dependency monitoring
* Application Insights integration

---

# Repository Structure

```text
enterprise-ai-agent/
│
├── api/                    # FastAPI application entrypoints
├── config/                 # Configuration management
├── db/                     # Database and storage integrations
├── middleware/             # Request middleware
├── routes/                 # API routes
├── services/               # Core business services
├── retrieval/              # Vector retrieval pipeline
├── observability/          # Logging and monitoring
├── experiments/            # Experimental scripts
├── tests/                  # Testing modules
├── .github/workflows/      # CI/CD pipelines
├── Dockerfile              # Container runtime
├── requirements.txt        # Python dependencies
└── README.md
```

---

# Environment Variables

## Core Platform

```env
OPENAI_API_KEY=
API_KEY=
ENABLE_INGESTION=false
MODEL_NAME=gpt-4.1-mini
TEMPERATURE=0.3
```

## Cosmos DB

```env
COSMOS_ENDPOINT=
COSMOS_KEY=
COSMOS_DATABASE=
COSMOS_CONTAINER=
COSMOS_SESSION_CONTAINER=
```

## Azure AI Search

```env
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_API_KEY=
AZURE_SEARCH_INDEX_NAME=
AZURE_SEARCH_API_VERSION=
```

## Azure Blob Storage

```env
AZURE_STORAGE_ACCOUNT=
AZURE_STORAGE_KEY=
AZURE_STORAGE_CONTAINER=
```

## Redis

```env
REDIS_CONNECTION_STRING=
```

---

# Local Development Setup

## 1. Clone Repository

```bash
git clone <repository-url>
cd enterprise-ai-agent
```

## 2. Create Virtual Environment

### Windows PowerShell

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment

Create:

```text
.env
```

Add required environment variables.

---

## 5. Start Application

```bash
uvicorn api.main:app --reload
```

---

# Docker Runtime

## Build Image

```bash
docker build -t enterprise-ai-agent .
```

## Run Container

```bash
docker run -it --rm -p 8000:8000 --env-file .env enterprise-ai-agent
```

---

# Health Endpoints

## Liveness Probe

```http
GET /health/live
```

Example Response:

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

Example Response:

```json
{
  "status": "ready",
  "checks": {
    "openai_api_key": true,
    "api_key": true,
    "redis": true
  }
}
```

---

# Deployment Architecture

## Staging Flow

```text
feature/* branch
        ↓
GitHub Actions CI/CD
        ↓
Docker Build
        ↓
Azure Container Registry
        ↓
Azure App Service (Staging)
        ↓
Readiness Validation
```

---

# GitHub Project Workflow

The engineering workflow is managed through a centralized GitHub Project board.

Workflow stages:

* Backlog
* Planned
* In Progress
* Blocked
* Testing
* Done
* Future

The project board tracks:

* frontend work
* backend work
* infrastructure
* observability
* deployment readiness
* roadmap execution

---

# Current Engineering Status

## Completed

* FastAPI backend foundation
* Health & readiness architecture
* Azure infrastructure integration
* CI/CD deployment pipelines
* Managed Identity integration
* RAG retrieval pipeline
* Cosmos memory persistence
* Application Insights integration
* Feature branch deployment strategy

## In Progress

* Frontend platform foundation
* Deployment smoke testing
* Container observability improvements
* Personalized tutoring capabilities

## Planned

* Retry & circuit breaker strategies
* Integration testing framework
* Monitoring dashboards
* Frontend chat experience
* Advanced tutor personalization

---

# Engineering Principles

The platform emphasizes:

* production-first engineering
* deployment validation
* observability-driven operations
* scalable architecture
* lightweight governance
* execution discipline

---

# Related Repositories

## Frontend Platform

Repository:

```text
enterprise-ai-frontend
```

Responsible for:

* React frontend
* Chat experience
* Streaming UI
* API integration layer
* User experience

---

# Future Roadmap

Planned future initiatives include:

* JWT authentication
* OAuth integration
* Hybrid search
* Circuit breaker strategies
* Integration testing
* Multi-tenant SaaS architecture
* Advanced AI personalization

---

# License

Private enterprise project.
