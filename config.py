from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY")
    DOCUMENT_PATH = ["data/★ 2024 노무관리 가이드 북.pdf", "data/근로기준법(법률)(제20520호)(20250223).pdf", "data/고용노동부-2025년부터-이렇게-달라집니다.pdf"]
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 50
    LLM_MODEL = "solar-pro"
    EMBEDDING_MODEL = "embedding-query"
    SESSION_ID = "rag123"

    @classmethod
    def validate(cls):
        if not cls.API_KEY:
            raise ValueError("API_KEY is not set in environment variables.")
        for path in cls.DOCUMENT_PATH:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Document not found at {path}")