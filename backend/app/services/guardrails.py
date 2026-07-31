from langchain_core.prompts import ChatPromptTemplate
from app.services.llm_service import llm_service

class NetworkingGuardrail:
    def __init__(self):
        self.llm = llm_service.get_llm()
        self.system_prompt = (
            "You are a binary classifier. Your only job is to determine if a user's question "
            "is related to Computer Networking (Cisco, routing, switching, protocols, IP, etc.).\n"
            "Respond ONLY with 'YES' or 'NO'. Do not explain."
        )

    def is_networking_related(self, question: str) -> bool:
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("user", f"Question: {question}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"question": question})
        content = response.content.strip().upper()
        
        return "YES" in content

guardrail = NetworkingGuardrail()