from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_upstage import UpstageEmbeddings
import logging
from config import Config

# 로깅 설정
logger = logging.getLogger(__name__)

class VectorStoreManager:

    def __init__(self, file_path=Config.DOCUMENT_PATH, chunk_size=Config.CHUNK_SIZE, chunk_overlap=Config.CHUNK_OVERLAP):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.vectorstore = None
        self._initialize()

    def _initialize(self):
        try:
            self.load_vectorstore()
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            logger.info("Creating new vector store")
            self.make_vectorstore()

    def load_vectorstore(self):
        logger.info("Loading FAISS vector store")
        try:
            logger.info("Creating embeddings")
            embeddings = UpstageEmbeddings(
                api_key=Config.API_KEY,
                model=Config.EMBEDDING_MODEL
            )
            logger.info("Load FAISS vector store")
            self.vectorstore = FAISS.load_local(
                folder_path="faiss_db",
                index_name="faiss_index",
                embeddings=embeddings,
                allow_dangerous_deserialization=True,
            )
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            raise
        
    def make_vectorstore(self):
        logger.info("Creating new FAISS vector store")
        try:
            logger.info(f"Loading document from {self.file_path}")
            loader = PyMuPDFLoader(self.file_path)
            docs = loader.load()

            logger.info("Splitting documents")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
            split_documents = text_splitter.split_documents(docs)

            logger.info("Creating embeddings")
            embeddings = UpstageEmbeddings(
                api_key=Config.API_KEY,
                model=Config.EMBEDDING_MODEL
            )

            logger.info("Building FAISS vector store")
            self.vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)
            self.vectorstore.save_local(folder_path="faiss_db", index_name="faiss_index")
            logger.info("FAISS vector store saved successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            raise

    def get_vectorstore(self):
        if self.vectorstore is None:
            raise ValueError("Vector store is not initialized.")
        return self.vectorstore

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    vector_store_manager = VectorStoreManager()
    vector_store = vector_store_manager.get_vectorstore()
    logger.info("Vector store is ready for use.")
