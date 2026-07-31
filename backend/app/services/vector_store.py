from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings
import os

class VectorStoreService:
    def __init__(self):
        # WARM UP: Load the model immediately into RAM
        print("🚀 WARMING UP: Loading Local Embedding Model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
        self.vector_db = None
        # Trigger an empty search to force-load the model into memory
        try:
            self.embeddings.embed_query("warmup")
            print("✅ Embedding Engine Ready.")
        except:
            pass

    def get_vector_store(self):
        if self.vector_db is None:
            self.vector_db = Chroma(
                persist_directory=settings.CHROMA_DB_DIR,
                embedding_function=self.embeddings,
                collection_name="networking_kb"
            )
        return self.vector_db

    def ingest_documents(self):
        from app.services.document_processor import doc_processor
        chunks = doc_processor.process_directory()
        if chunks:
            db = self.get_vector_store()
            db.add_documents(chunks)
            print("✅ Knowledge Base Ingested.")

vector_service = VectorStoreService()