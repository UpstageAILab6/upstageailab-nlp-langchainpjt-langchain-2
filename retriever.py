import logging
from vector_store import VectorStoreManager

# 로깅 설정
logger = logging.getLogger(__name__)

class Retriever:
    
    def __init__(self, vector_store_manager: VectorStoreManager):
        try:
            logger.info("Initializing retriever from vector store")
            self.retriever = vector_store_manager.get_vectorstore().as_retriever()
        except Exception as e:
            logger.error(f"Failed to initialize retriever: {str(e)}")
            raise

    def get_retriever(self):
        """Retrieve the configured retriever."""
        return self.retriever

__all__ = ["Retriever"]