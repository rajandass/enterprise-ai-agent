# Enterprise AI Platform — Full System Rebuild Guide

## Version
v1.0

## Purpose
This document is a complete implementation and operational guide for recreating the Enterprise AI Platform from scratch.

The guide includes:
- frontend architecture
- backend architecture
- cloud infrastructure
- CI/CD pipelines
- Docker setup
- Azure deployment
- security configuration
- happy-path setup
- common failure scenarios
- debugging guidance

This document is intended for:
- developers
- DevOps engineers
- AI engineers
- solution architects

---

# 🚀 System Overview

## Platform Purpose
Enterprise-grade AI support platform with:
- streaming AI responses
- persistent conversations
- citations
- session memory
- cloud-native deployment
- enterprise DevOps

---

# 🏗️ High-Level Architecture

```text
Next.js Frontend
        ↓
FastAPI Backend API
        ↓
OpenAI APIs
Cosmos DB
Redis Cache
Azure Key Vault
```

---

# ☁️ Cloud Architecture

```text
GitHub Actions
        ↓
Docker Build
        ↓
Azure Container Registry
        ↓
Azure App Service
```

---

# 🚀 Technology Stack

## Frontend
- Next.js 15
- React
- TypeScript
- Tailwind CSS
- React Markdown

## Backend
- FastAPI
- Python
- LangChain
- OpenAI SDK
- Redis
- Azure Cosmos DB

## Cloud
- Azure App Service
- Azure Container Registry
- Azure Key Vault
- Azure Cosmos DB
- Azure Redis
- Application Insights

## DevOps
- Docker
- GitHub Actions
- Branch protection
- Approval-based deployments

---

# 📁 Repository Structure

## Frontend Repository

```text
enterprise-ai-frontend/
│
├── app/
├── public/
├── .github/workflows/
├── Dockerfile
├── package.json
└── README.md
```

---

## Backend Repository

```text
enterprise-ai-agent/
│
├── api/
├── services/
├── db/
├── ingestion/
├── cache/
├── utils/
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 🚀 FRONTEND IMPLEMENTATION

# 1. Frontend Features

## Completed Features
- streaming responses
- persistent chat history
- conversation sidebar
- new chat workflow
- citations rendering
- markdown rendering
- session persistence
- production deployment

---

# 2. Frontend Environment Variables

## Local Development

Create:

```text
.env.local
```

Add:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_KEY=your-api-key
```

---

# 3. Frontend Local Development

## Install Dependencies

```bash
npm install
```

---

## Run Development Server

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:3000
```

---

# 4. Frontend Docker Setup

## Build Docker Image

```bash
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 \
  --build-arg NEXT_PUBLIC_API_KEY=your-api-key \
  -t enterprise-ai-frontend .
```

---

## Run Frontend Container

```bash
docker run -p 3000:3000 enterprise-ai-frontend
```

---

# 🚀 BACKEND IMPLEMENTATION

# 5. Backend Features

## Completed Features
- /ask endpoint
- /ask-stream endpoint
- streaming responses
- OpenAI integration
- Redis caching
- Cosmos DB persistence
- conversation APIs
- citations
- rate limiting
- request tracing
- API key authentication

---

# 6. Backend Environment Variables

Create:

```text
.env
```

Add:

```env
OPENAI_API_KEY=
OPENAI_MODEL=
API_KEY=

REDIS_HOST=localhost
REDIS_PORT=6379

COSMOS_ENDPOINT=
COSMOS_KEY=
COSMOS_DATABASE=
COSMOS_CONTAINER=
COSMOS_SESSION_CONTAINER=
```

---

# 7. Backend Local Development

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Environment

### Windows

```powershell
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# 8. Backend Docker Setup

## Build Backend Image

```bash
docker build -t enterprise-ai-backend .
```

---

## Run Backend Container

```bash
docker run -p 8000:8000 enterprise-ai-backend
```

---

# 🚀 REDIS SETUP

# 9. Redis Container

## Start Redis

```bash
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis
```

---

## Verify Redis

```bash
docker ps
```

---

# ☁️ AZURE INFRASTRUCTURE

# 10. Azure Resources

## Required Services

| Service | Purpose |
|---|---|
| Azure App Service | frontend hosting |
| Azure App Service | backend hosting |
| Azure Container Registry | Docker images |
| Azure Cosmos DB | persistent chat storage |
| Azure Redis Cache | caching |
| Azure Key Vault | secrets |
| Application Insights | monitoring |

---

# 11. Azure Resource Group

## Create Resource Group

```bash
az group create \
  --name ai-agent-rg \
  --location eastus
```

---

# 12. Azure Container Registry

## Create ACR

```bash
az acr create \
  --resource-group ai-agent-rg \
  --name enterpriseaiacr12345 \
  --sku Basic
```

---

## Enable Admin Access

```bash
az acr update \
  --name enterpriseaiacr12345 \
  --admin-enabled true
```

---

# 13. Azure App Service

## Frontend App

```text
enterprise-ai-ui-prod-12345
```

---

## Backend App

```text
ai-agent-app-12345
```

---

# 🔐 SECURITY IMPLEMENTATION

# 14. Azure Key Vault

## Key Vault Name

```text
ai-agent-kv-12345
```

---

## Managed Identity

Enable:

```text
System Assigned Managed Identity
```

for backend App Service.

---

## Store Cosmos Secret

```bash
az keyvault secret set \
  --vault-name ai-agent-kv-12345 \
  --name COSMOS-KEY \
  --value "YOUR_COSMOS_KEY"
```

---

## Key Vault Reference

```bash
az webapp config appsettings set \
  --name ai-agent-app-12345 \
  --resource-group ai-agent-rg \
  --settings \
  COSMOS_KEY='@Microsoft.KeyVault(SecretUri=https://ai-agent-kv-12345.vault.azure.net/secrets/COSMOS-KEY/)'
```

---

# 🚀 FRONTEND CI/CD

# 15. Frontend GitHub Secrets

Required:

| Secret | Purpose |
|---|---|
| AZURE_WEBAPP_NAME | frontend app service |
| AZURE_RESOURCE_GROUP | resource group |
| AZURE_ACR_USERNAME | ACR auth |
| AZURE_ACR_PASSWORD | ACR auth |
| NEXT_PUBLIC_API_URL | backend URL |
| NEXT_PUBLIC_API_KEY | frontend auth |
| AZURE_WEBAPP_PUBLISH_PROFILE | deployment auth |

---

# 16. Frontend GitHub Actions

Workflow:

```text
.github/workflows/frontend-deploy.yml
```

Pipeline:
- Docker build
- ACR push
- approval gate
- Azure deployment

---

# 🚀 BACKEND CI/CD

# 17. Backend Deployment Pipeline

Backend already uses:
- GitHub Actions
- Docker deployment
- Azure App Service deployment

---

# 🌐 CORS CONFIGURATION

# 18. Backend CORS

Required:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://enterprise-ai-ui-prod-12345.azurewebsites.net"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

# 🚀 HAPPY PATH FLOW

# 19. Local Development Happy Path

## Backend

1. Start Redis
2. Activate venv
3. Install requirements
4. Run FastAPI backend

---

## Frontend

1. Install npm packages
2. Configure .env.local
3. Start Next.js frontend

---

## Validation

Frontend:

```text
http://localhost:3000
```

Backend Swagger:

```text
http://localhost:8000/docs
```

Expected:
- conversations load
- streaming works
- citations render
- persistent chats save

---

# 20. Production Happy Path

## Deployment Flow

```text
feature branch
    ↓
pull request
    ↓
merge to main
    ↓
GitHub Actions
    ↓
Docker build
    ↓
push to ACR
    ↓
approval gate
    ↓
Azure App Service deployment
```

---

## Production Validation

Expected:
- frontend loads
- backend responds
- conversations persist
- citations display
- streaming works
- sidebar loads

---

# 🚨 ERROR PATHS & DEBUGGING

# 21. Common Frontend Errors

## Issue

```text
401 Unauthorized
```

### Cause
API key mismatch.

### Fix
Verify:

```env
NEXT_PUBLIC_API_KEY
```

matches backend:

```env
API_KEY
```

---

## Issue

```text
localhost API failing in production
```

### Cause
Frontend built with:

```text
http://localhost:8000
```

### Fix
Rebuild frontend using production backend URL.

---

# 22. Common Backend Errors

## Issue

```text
Redis connection refused
```

### Cause
Redis container not running.

### Fix

```bash
docker start redis
```

---

## Issue

```text
ModuleNotFoundError: azure.cosmos
```

### Cause
Dependency missing from:

```text
requirements.txt
```

### Fix
Add:

```text
azure-cosmos
```

---

## Issue

```text
CORS blocked
```

### Cause
Production frontend missing from allowed origins.

### Fix
Update CORS middleware.

---

## Issue

```text
Conversation APIs return 404
```

### Cause
Production backend running outdated deployment.

### Fix
Push latest backend changes and redeploy.

---

# 23. Azure Deployment Issues

## Issue

```text
Container startup failed
```

### Cause
Missing environment variables or missing dependencies.

### Fix
Check logs:

```bash
az webapp log tail \
  --name ai-agent-app-12345 \
  --resource-group ai-agent-rg
```

---

## Issue

```text
App Service blocked after repeated startup failures
```

### Cause
Container crashes repeatedly.

### Fix
Resolve startup error and restart App Service.

---

# 24. Debugging Checklist

## Backend

Verify:
- Redis running
- Cosmos env vars exist
- Key Vault references valid
- requirements.txt complete
- Docker image rebuilt
- CORS configured

---

## Frontend

Verify:
- correct API URL
- correct API key
- Docker image rebuilt
- production environment variables correct

---

## Azure

Verify:
- App Service healthy
- ACR accessible
- Managed Identity enabled
- Key Vault access granted

---

# 🚀 FINAL SYSTEM CAPABILITIES

## Current Production Features

- streaming AI responses
- persistent conversations
- citations
- conversation sidebar
- Cosmos DB persistence
- Redis caching
- Dockerized architecture
- Azure deployment
- CI/CD automation
- Key Vault security
- Managed Identity integration

---

# 🚀 NEXT EVOLUTION

Recommended next feature:

```text
Document Upload + Multi-Document RAG
```

This transforms the platform into a true enterprise knowledge assistant.

