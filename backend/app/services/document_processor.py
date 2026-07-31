from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.config import settings
import os

class DocumentProcessor:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def process_directory(self):
        """Loads all PDFs and returns split chunks."""
        if not os.path.exists(settings.KNOWLEDGE_BASE_DIR):
            os.makedirs(settings.KNOWLEDGE_BASE_DIR)
            return []

        loader = DirectoryLoader(
            settings.KNOWLEDGE_BASE_DIR,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader
        )
        
        documents = loader.load()
        chunks = self.splitter.split_documents(documents)
        print(f"✅ Processed {len(documents)} documents into {len(chunks)} chunks.")
        return chunks

doc_processor = DocumentProcessor()