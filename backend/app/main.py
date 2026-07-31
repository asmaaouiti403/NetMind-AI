from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.rag_engine import rag_engine
from app.services.vector_store import vector_service
import uvicorn

app = FastAPI()

# FORCE ALLOW EVERYTHING FOR DEMO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    # THIS IS THE CRITICAL LOG
    print(f"\n📢 [BACKEND] I just received a message: {request.question}")
    try:
        response = rag_engine.get_answer(request.question)
        print(f"✅ [BACKEND] Generated response successfully.")
        return response
    except Exception as e:
        print(f"❌ [BACKEND] Internal Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ingest")
async def ingest():
    print("📂 [BACKEND] Ingesting documents...")
    vector_service.ingest_documents()
    return {"status": "success"}

@app.get("/health")
def health():
    return {"status": "online"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)