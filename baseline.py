# 업스테이지 라이브러리 사용하기 위해 필요한 transformers 와 tokenizers 버전
# tokenizers-0.19.1
# transformers-4.41.0

# pip install langchain_text_splitters
# pip install langchain_community
# pip install pymupdf
# pip install -qU langchain-core langchain-upstage
# pip install faiss-cpu

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_upstage import ChatUpstage, UpstageEmbeddings
<<<<<<< HEAD

# 단계 1: 문서 로드(Load Documents)
# pdf 파일 다운로드 링크: https://spri.kr/posts/view/23669
loader = PyMuPDFLoader("data/SPRI_AI_Brief_2023년12월호_F.pdf")
=======
from dotenv import load_dotenv
import utils

load_dotenv()

# 단계 1: 문서 로드(Load Documents)
# pdf 파일 다운로드 링크: https://spri.kr/posts/view/23669
pdf_file_path = "./data/근로기준법(법률)(제20520호)(20250223).pdf"
loader = PyMuPDFLoader(pdf_file_path)
>>>>>>> bfe289e (add function base code)
docs = loader.load()

# 단계 2: 문서 분할(Split Documents)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
split_documents = text_splitter.split_documents(docs)

# 단계 3: 임베딩(Embedding) 생성
embeddings = UpstageEmbeddings(
<<<<<<< HEAD
    api_key="",
=======
    api_key=utils.load_api_key(),
>>>>>>> bfe289e (add function base code)
    model="embedding-query"
)

# 단계 4: DB 생성(Create DB) 및 저장
# 벡터스토어를 생성합니다.
vectorstore = FAISS.from_documents(documents=split_documents, embedding=embeddings)

# 단계 5: 검색기(Retriever) 생성
# 문서에 포함되어 있는 정보를 검색하고 생성합니다.
retriever = vectorstore.as_retriever()

# 단계 6: 프롬프트 생성(Create Prompt)
# 프롬프트를 생성합니다.
prompt = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. 
Answer in Korean.

#Question: 
{question} 
#Context: 
{context} 

#Answer:"""
)

# 단계 7: 언어모델(LLM) 생성
# 모델(LLM) 을 생성합니다.
<<<<<<< HEAD
llm = ChatUpstage(api_key="", model="solar-pro")
=======
llm = ChatUpstage(api_key=utils.load_api_key(), model="solar-pro")
>>>>>>> bfe289e (add function base code)

# 단계 8: 체인(Chain) 생성
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 체인 실행(Run Chain)
# 문서에 대한 질의를 입력하고, 답변을 출력합니다.
<<<<<<< HEAD
question = "삼성전자가 자체 개발한 AI 의 이름은?"
=======
question = "퇴직금은 1년 미만 근무해도 받을 수 있나요?"
>>>>>>> bfe289e (add function base code)
response = chain.invoke(question)
print(response)
