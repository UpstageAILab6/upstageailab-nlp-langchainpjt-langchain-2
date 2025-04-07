from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_upstage import UpstageEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
import logging
from config import Config
import re

# 로깅 설정
logger = logging.getLogger(__name__)

class VectorStoreManager:

    def __init__(self, file_paths=Config.DOCUMENT_PATH, chunk_size=Config.CHUNK_SIZE, chunk_overlap=Config.CHUNK_OVERLAP):
        self.file_paths = file_paths
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
            logger.info("Load FAISS vector store...")
            self.vectorstore = FAISS.load_local(
                folder_path="faiss_db",
                index_name="faiss_index",
                embeddings=embeddings,
                allow_dangerous_deserialization=True,
            )
            logger.info("Load FAISS vector store successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {str(e)}")
            raise

    def make_vectorstore(self):
        def clean_text1(text, i):
            # ■ 제거
            text = text.replace("■", "")
            if i in [1,2]:
                pass
            else:
                # 페이지 제거
                text = re.sub(r"\d+\s*노무관리\s가이드\s북", "", text)
                
                text = re.sub(r"1\.\s*근로조건\s서면명시\s*\d+", "", text)
                text = re.sub(r"2\.\s*근로자\s명부\s및\s계약서류\s보존\s*\d+", "", text)
                text = re.sub(r"3\.\s*임금\s등\s각종\s금품\s지급\s*\d+", "", text)
                text = re.sub(r"4\.\s*근로시간\s및\s연장근로\s한도\s위반\s*\d+", "", text)
                text = re.sub(r"5\.\s*휴게시간\s부여\s*\d+", "", text)
                text = re.sub(r"6\.\s*유급휴일\s부여\s*\d+", "", text)
                text = re.sub(r"7\.\s*연차유급휴가\s부여\s*\d+", "", text)
                text = re.sub(r"8\.\s*연소자와\s모성\s보호\s*\d+", "", text)
                text = re.sub(r"9\.\s*취업규칙s*\d+", "", text)
                text = re.sub(r"10\.\s*퇴직급여\s지급\s*\d+", "", text)
                text = re.sub(r"11\.\s*직장\s내\s괴롭힘\s예방\s*\d+", "", text)
                text = re.sub(r"12\.\s*최저임금\s준수\s*\d+", "", text)
                text = re.sub(r"13\.\s*직장\s내\s성희롱\s예방\s*\d+", "", text)
                text = re.sub(r"14\.\s*고용상\s성차별\s금지\s*\d+", "", text)
                text = re.sub(r"15\.\s*비정규직\s차별\s금지\s*\d+", "", text)
                text = re.sub(r"16\.\s*노사협의회\s설치·운영\s*\d+", "", text)

            return text

        
        def clean_text2(text, i):
            if i == 0:
                first_index = text.find("근로기준법")
                if first_index != -1:
                    # 처음 '근로기준법'은 남겨두고, 나머지 부분에서 모두 제거
                    before = text[:first_index + len("근로기준법")]
                    after = text[first_index + len("근로기준법"):].replace("근로기준법", "")
                    text = before + after
            
            else:
                text = re.sub(r'\s*근로기준법\s*', '', text)

            text = re.sub(r"법제처\s*\d+\s*국가법령정보센터", '', text)

            return text

        
        def clean_text3(text, i):
            text =  re.sub(r'\s*-\s*\d+\s*-\s*', ' ', text)
            
            return text


        logger.info("Creating new FAISS vector store")
        try:
            logger.info(f"Loading document from {self.file_paths}")

            # text_splitter = RecursiveCharacterTextSplitter(
            #     chunk_size=self.chunk_size,
            #     chunk_overlap=self.chunk_overlap
            # )
            
            logger.info("Creating embeddings")
            embeddings = UpstageEmbeddings(
                api_key=Config.API_KEY,
                model=Config.EMBEDDING_MODEL
            )
            # 안전 분할용 splitter (토큰 길이 고려하려면 chunk_size=1500~2000 등)
            safe_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

            logger.info("Using SemanticChunker with Upstage Embeddings for chunking")
            semantic_chunker = SemanticChunker(embeddings)

            all_split_documents = []
            for file_path in self.file_paths:
                loader = PyMuPDFLoader(file_path)
                docs = loader.load()
                logger.info(f"Loaded {file_path}, splitting documents...")
                # split_docs = text_splitter.split_documents(docs)
                
                # 1) 먼저 safe split
                safe_docs = safe_splitter.split_documents(docs)

                # 2) semantic chunker
                split_docs = semantic_chunker.split_documents(safe_docs)

                # 혹은 split_docs에서 빈 문자열 Document 체크
                final_docs = [d for d in split_docs if d.page_content.strip()]

                all_split_documents.extend(split_docs)

            logger.info("Building FAISS vector store")
            self.vectorstore = FAISS.from_documents(documents=all_split_documents, embedding=embeddings)
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