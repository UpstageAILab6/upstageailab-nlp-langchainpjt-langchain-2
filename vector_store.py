from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_upstage import UpstageEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

# 단계 1: 문서 로드(Load Documents)
loader = PyMuPDFLoader("./data/★ 2024 노무관리 가이드 북.pdf")
docs = loader.load()

# 단계 2: 문서 분할(Split Documents)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
split_documents = text_splitter.split_documents(docs)

# 단계 3: 임베딩(Embedding) 생성
embeddings = UpstageEmbeddings(
    api_key=os.getenv('API_KEY'),
    model="embedding-query"
)

# 단계 4: DB 생성(Create DB) 및 저장
# 벡터스토어를 생성합니다.
vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

__all__ = ["vectorstore"]  # 외부에서 사용할 수 있도록 추가


