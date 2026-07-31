from langchain_groq import ChatGroq
from app.core.config import settings

class LLMService:
    def __init__(self):
        # We use the settings object which now has the fixed key
        if not settings.GROQ_API_KEY:
            print("CRITICAL ERROR: Groq API Key is not set in config.")
            
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=settings.GROQ_API_KEY,
            model_name=settings.MODEL_NAME
        )

    def get_llm(self):
        return self.llm

llm_service = LLMService()