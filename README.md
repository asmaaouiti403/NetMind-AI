# NetMind AI
### RAG-Powered Networking AI Assistant

NetMind AI is a specialized Artificial Intelligence assistant designed for computer networking expertise. It utilizes Retrieval-Augmented Generation (RAG) to provide grounded technical support, protocol analysis, and troubleshooting guidance based on a dedicated networking knowledge base.

---

## Overview

The system is a specialized Large Language Model (LLM) application that processes technical networking documentation and official RFCs to provide accurate, non-hallucinated technical support.

*   **Semantic Retrieval:** Uses a Vector Database to retrieve facts from technical PDF documentation.
*   **Domain Specific:** Strict guardrails prevent the AI from answering non-networking questions, ensuring its role as a professional tool.
*   **High Performance:** Leverages Cloud LPU technology for near-instant response times.
*   **Citations:** Every answer includes clickable links to the original source documentation for technical verification.

---

## Technical Stack

### Backend (AI Engine)
*   Framework: FastAPI (Python 3.12)
*   Orchestration: LangChain
*   Vector Store: ChromaDB
*   Embeddings: BAAI/bge-small-en-v1.5
*   Inference: Groq Cloud API (Llama 3.3-70B)

### Frontend (User Interface)
*   Framework: React.js
*   Styling: Tailwind CSS (Tactical Slate/Blue Theme)
*   Icons: Lucide-React
*   Persistence: LocalStorage for session history management.

---

## Project Structure

```text
net-ai-assistant/
├── backend/
│   ├── app/
│   │   ├── core/           # Configuration, Prompts, and Constants
│   │   ├── services/       # RAG Engine, Vector Store, LLM Logic
│   │   └── main.py         # FastAPI Entry Point
│   ├── knowledge_base/     # Technical PDFs and RFCs
│   ├── data/               # Persistent ChromaDB storage
│   └── .env                # API Keys and Model Config
├── frontend/
│   ├── src/                # React Components & Logic
│   └── package.json        # Dependencies
└── README.md

Setup and Installation

1. Backend Setup

cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000

2. Knowledge Base Ingestion

To populate the AI's memory:

curl -X POST http://127.0.0.1:8000/api/ingest

3. Frontend Setup

cd frontend
npm install
npm start

Core Logic

  - Intent Guardrail: The system identifies non-networking queries and triggers
    a refusal protocol: "I specialize in computer networking and cannot answer
    questions outside this field."
  - Plain Text Enforcement: Custom regex cleaning ensures technical data is
    delivered in a clean format without markdown symbols.
  - LPU Optimization: Utilizes Groq's Language Processing Units for sub-second
    inference speeds.



