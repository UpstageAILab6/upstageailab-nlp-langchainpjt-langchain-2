from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_upstage import UpstageEmbeddings
<<<<<<< HEAD
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


=======
import utils

def load_pdf_documents(file_path):
    """
    PDF 문서를 로드합니다.
    :param file_path: PDF 파일 경로
    :return: 로드된 문서
    """
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()
    return docs

def split_documents(docs, chunk_size=1000, chunk_overlap=50):
    """
    문서를 분할합니다.
    :param docs: 로드된 문서
    :param chunk_size: 분할 크기
    :param chunk_overlap: 중첩 크기
    :return: 분할된 문서
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_docs = text_splitter.split_documents(docs)
    return split_docs

def create_vectorstore(split_docs, api_key, model="embedding-query"):
    """
    벡터스토어를 생성합니다.
    :param split_docs: 분할된 문서
    :param api_key: API 키
    :param model: 모델 이름
    :return: 생성된 벡터스토어
    """
    embeddings = UpstageEmbeddings(api_key=api_key, model=model)
    vectorstore = FAISS.from_documents(documents=split_docs, embedding=embeddings)
    return vectorstore

# TODO: add save vectorstore to disk
def get_vectorstore(pdf_file_path, chunk_size=1000, chunk_overlap=50):
    """
    벡터스토어를 가져옵니다.
    :return: 벡터스토어
    """
    # 단계 1: 문서 로드
    docs = load_pdf_documents(pdf_file_path)

    # 단계 2: 문서 분할
    split_docs = split_documents(docs, chunk_size, chunk_overlap)

    # 단계 3: 벡터스토어 생성
    vectorstore = create_vectorstore(split_docs, utils.load_api_key())

    return vectorstore

if __name__ == "__main__":
    # PDF 파일 경로
    pdf_file_path = "./data/근로기준법(법률)(제20520호)(20250223).pdf"

    # 벡터스토어 생성
    vectorstore = get_vectorstore(pdf_file_path)
>>>>>>> bfe289e (add function base code)
