import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Force reload the .env file from the disk
load_dotenv(override=True)

class Settings(BaseSettings):
    APP_NAME: str = "NetMind AI Assistant"
    
  
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
    
    CHROMA_DB_DIR: str = os.path.join(os.getcwd(), "data", "chroma")
    KNOWLEDGE_BASE_DIR: str = os.path.join(os.getcwd(), "knowledge_base")
    
    REFUSAL_MESSAGE: str = "I'm a networking assistant and can only answer questions related to computer networking."

settings = Settings()

# Debugging: This will print in your terminal when you start the backend
if settings.GROQ_API_KEY:
    print("✅ Config: Groq API Key loaded successfully.")
else:
    print("❌ Config: Groq API Key is MISSING!")