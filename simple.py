import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableLambda
from operator import itemgetter

# 환경 변수 로드
load_dotenv()
API_KEY = os.getenv("API_KEY")

# 문서 로드 및 벡터 저장소 생성
# loader = PyMuPDFLoader("./data/★ 2024 노무관리 가이드 북.pdf")
# docs = loader.load()
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
# split_docs = text_splitter.split_documents(docs)
embeddings = UpstageEmbeddings(api_key=API_KEY, model="embedding-query")
# vectorstore = FAISS.from_documents(split_docs, embedding=embeddings)
vectorstore = FAISS.load_local()
retriever = vectorstore.as_retriever()

# LLM 및 프롬프트 설정
llm = ChatUpstage(api_key=API_KEY, model="solar-pro")
prompt = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Answer in Korean.

#Previous Chat History:
{chat_history}

#Question:
{question}
#Context:
{context}

#Answer:"""
)

# 체인 구성 (프롬프트 확인 추가)
chain = (
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "chat_history": itemgetter("chat_history"),
    }
    | prompt
    | RunnableLambda(lambda x: (print("완성된 프롬프트:\n", x.text), x)[1])  # 프롬프트 출력
    | llm
    | StrOutputParser()
)

# 대화 기록 관리
store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
        store[session_id].add_message = lambda msg: [
            store[session_id].messages.append(msg),
            store[session_id].messages.__setitem__(slice(0, len(store[session_id].messages) - 10, None), [])
        ][0] if len(store[session_id].messages) <= 10 else store[session_id].messages.__setitem__(slice(0, 1, None), [])
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# 메인 실행 루프
SESSION_ID = "rag123"
while True:
    question = input("질문을 입력하세요 (종료하려면 'exit' 입력): ")
    if question.lower() == "exit":
        break
    response = chain_with_history.invoke(
        {"question": question},
        config={"configurable": {"session_id": SESSION_ID}},
    )
    print("답변:", response)