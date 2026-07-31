import re
from app.services.llm_service import llm_service
from app.services.vector_store import vector_service
from app.core.prompts import SYSTEM_PROMPT
from app.core.constants import RFC_MAP
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class RAGEngine:
    def __init__(self):
        self.llm = llm_service.get_llm()
        self.vector_db = vector_service.get_vector_store()

    def get_answer(self, question: str):
        # 1. IMMEDIATE GREETING RETURN
        q = question.lower().strip()
        if q in ["hi", "hello", "hey"]:
            return {"answer": "Hello! I am NetMind AI, how can I help with your networking query?", "sources": []}

        # 2. PROCEED TO RAG: RETRIEVAL
        docs = self.vector_db.similarity_search(question, k=3)
        context = "\n\n".join([d.page_content for d in docs])
        
        # 3. BUILD PROMPT
        prompt_template = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
        
        # --- PROOF: PRINTING THE RAG PIPELINE DATA ---
        print("\n" + "="*50)
        print("RAG PIPELINE DEBUG: RETRIEVED CONTEXT")
        print("="*50)
        print(context) 
        print("="*50 + "\n")
        # ----------------------------------------------

        chain = prompt_template | self.llm | StrOutputParser()
        
        # 4. GENERATION
        response = chain.invoke({"context": context, "question": question})

        # 5. CLEANING LOGIC
        clean_response = response.replace("*", "").replace("#", "").replace("_", "")
        clean_response = re.sub(r'\n\s*\n', '\n\n', clean_response).strip()

        sources = []
        if "cannot answer" not in response:
            for d in docs:
                fname = d.metadata.get("source", "").split("/")[-1]
                if fname not in [s['name'] for s in sources]:
                    sources.append({"name": fname, "url": RFC_MAP.get(fname, "#")})

        return {"answer": clean_response, "sources": sources}

rag_engine = RAGEngine()