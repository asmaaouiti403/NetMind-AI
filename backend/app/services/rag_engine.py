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

        # 2. PROCEED TO RAG
        docs = self.vector_db.similarity_search(question, k=3)
        context = "\n\n".join([d.page_content for d in docs])
        
        prompt = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
        chain = prompt | self.llm | StrOutputParser()
        response = chain.invoke({"context": context, "question": question})

        # --- 🏁 THE AGGRESSIVE CLEANER 🏁 ---
        # Removes hashtags, asterisks, underscores, and plus signs
        clean_text = re.sub(r'[#*_+\xa0]', '', response) 
        
        # Ensures your structure markers stay clear
        clean_text = clean_text.replace("Note:", "\nSUMMARY\n")
        
        # Final cleanup of white space
        clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text).strip()

        # 3. SOURCE MAPPING
        sources = []
        # We only show sources if the AI didn't refuse the question
        if "specialize in computer networking" not in response.lower():
            for d in docs:
                fname = d.metadata.get("source", "").split("/")[-1]
                if fname not in [s['name'] for s in sources]:
                    sources.append({"name": fname, "url": RFC_MAP.get(fname, "#")})

        return {"answer": clean_text, "sources": sources}

# 🛠️ THIS IS THE MISSING LINE THAT FIXES THE ERROR:
rag_engine = RAGEngine()