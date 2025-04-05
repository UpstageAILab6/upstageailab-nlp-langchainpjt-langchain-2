from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY")
    DOCUMENT_PATH = "./data/★ 2024 노무관리 가이드 북.pdf"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 50
    LLM_MODEL = "solar-pro"
    EMBEDDING_MODEL = "embedding-query"
    SESSION_ID = "rag123"

    @classmethod
    def validate(cls):
        if not cls.API_KEY:
            raise ValueError("API_KEY is not set in environment variables.")
        if not os.path.exists(cls.DOCUMENT_PATH):
            raise FileNotFoundError(f"Document not found at {cls.DOCUMENT_PATH}")