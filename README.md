# 🚀 Enterprise AI Support Agent (Production-Grade RAG System)

## 📌 Overview

This project is a **production-ready Retrieval-Augmented Generation (RAG) system** that answers enterprise queries using internal documents.

It demonstrates:

* AI system design (not just API usage)
* RAG architecture
* Performance optimization
* Cost tracking
* Hallucination detection
* API deployment readiness

---

## 🧠 Key Features

* ✅ Retrieval-Augmented Generation (RAG)
* ✅ FastAPI-based API service
* ✅ Vector database (Chroma)
* ✅ LLM integration (OpenAI)
* ✅ Caching (instant repeat queries)
* ✅ Token usage & cost tracking
* ✅ Latency monitoring
* ✅ Confidence scoring (LLM verification)
* ✅ Source attribution (citations)

---

## 🏗️ Architecture

User → API → Retrieval → LLM → Verification → Response

---

## ⚙️ Tech Stack

* Python
* FastAPI
* LangChain
* ChromaDB
* OpenAI (GPT-4o-mini)
* Uvicorn

---

## 📂 Project Structure

```
enterprise-ai-agent/
│
├── api/                # FastAPI application
├── pipelines/          # RAG pipelines (ingestion + query)
├── evaluation/         # Evaluation scripts
├── data/               # Sample documents
├── models/             # Vector DB (ignored in git)
├── .env                # API keys (ignored)
├── README.md
```

---

## 🚀 How to Run

### 1. Setup environment

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add API Key

Create `.env`:

```
OPENAI_API_KEY=your_key_here
```

### 3. Run ingestion

```
python pipelines/ingestion.py
```

### 4. Start API

```
uvicorn api.main:app --reload
```

### 5. Test API

Open:

```
http://127.0.0.1:8000/docs
```

---

## 📊 Sample API Response

```
{
  "request_id": "uuid",
  "answer": "Employees are entitled to 20 days...",
  "confidence": "HIGH",
  "latency": 2.36,
  "tokens": 101,
  "cost": 0.000015,
  "citations": ["data/company_docs.txt"]
}
```

---

## 💰 Cost Efficiency

* ~100 tokens per query
* ~$0.000015 per request
* ~1M queries ≈ $15

---

## 🔍 Observability

* Latency tracking
* Token usage tracking
* Cost estimation
* Cache hit detection

---

## 🧠 Hallucination Control

* LLM-based verification layer
* Confidence scoring (HIGH / MEDIUM / LOW)
* Context-grounded answers only

---

## 📈 Future Improvements

* Redis caching
* Streaming responses
* Async pipeline
* Azure deployment
* CI/CD integration

---

## 👨‍💻 Author

Built as a **production-grade AI system** to demonstrate real-world AI engineering capabilities.

---

## ⭐ Key Takeaway

This is not a demo project.

It is a **deployable, scalable, and measurable AI system** aligned with real enterprise needs.
