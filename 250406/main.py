import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_upstage import ChatUpstage, UpstageEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from operator import itemgetter



basepath = os.path.dirname(__file__)
document_path = os.path.join(basepath, "data/2025년 4월 25일 인기 아이돌 상세 정보.txt")
vectorstore_path = os.path.join(basepath, "vectorstore")
print(basepath, document_path)


# upstage model use
embeddings = UpstageEmbeddings(api_key=os.getenv("API_KEY"), model="embedding-query")
llm = ChatUpstage(api_key=os.getenv("API_KEY"), model="solar-pro")


# vectorstore 로드 or 생성
is_load_vectorstore = True

if is_load_vectorstore:
    vector_store = FAISS.load_local(vectorstore_path, embeddings=embeddings, allow_dangerous_deserialization=True)
else:
    # 문서 로드
    loader = TextLoader(document_path, encoding="utf-8")
    documents = loader.load()
    print(documents[0].page_content[:50],"...")

    # 텍스트 split
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " "], chunk_size=200, chunk_overlap=20)
    docs = text_splitter.split_documents(documents=documents)

    # for doc in docs:
    #     print(doc.page_content)
    # exit()

    # 임베딩, 저장
    vector_store = FAISS.from_documents(documents=docs, embedding=embeddings)
    vector_store.save_local(vectorstore_path)

if not vector_store:
    print("vector_store not loaded")
    exit()


# 검색기로 변환
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k":2}
)


prompt = PromptTemplate.from_template("""
당신은 고도로 지능적인 QA 엔진입니다. 제공된 문서 참조 내용과 이전 대화 내용을 바탕으로 사용자의 질문에 답변하세요. 답변은 다음 지침을 따르세요:
1. 문서 참조 내용과 이전 대화 내용을 우선적으로 활용해 정확한 답변을 제공.
2. 문서나 대화에 정보가 부족하면, 일반 지식을 사용해 보완하되 출처가 다름을 명시.
3. 간결하고 명확하게 답변하며, 필요 시 간단한 설명 추가.

문서 참조 내용:
{context}

이전 대화 내용:
{history}

질문:
{question}
"""
)

# 대화 기록 저장소 (세션별)
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """세션 ID에 따라 대화 기록을 가져오거나 생성하며, 최대 10개 메시지로 제한"""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    history = store[session_id]
    if len(history.messages) > 10:
        history.messages = history.messages[-10:]
    return history


def get_formatted_history(messages):
    result = []
    for idx in range(0, len(messages), 2):
        result.append((f"USER: {messages[idx].content}", f"AI: {messages[idx+1].content}"))
    return result

# 체인 구성
chain = (
    {
        "context": itemgetter("question") | retriever | (lambda x: "\n".join(doc.page_content for doc in x)),
        "history": itemgetter("history") | RunnableLambda(get_formatted_history),
        "question": itemgetter("question")
    }
    | prompt
    # | RunnableLambda(lambda x: print(x) or x)
    | llm
    | StrOutputParser()
)

history_chain = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

session_id = "shayoyou"
querys = ["내 이름은 최영진이야", "블랙핑크 멤버", "에스파 멤버", "아이유 소속사", "소녀시대 리더", "지수를 제외한 멤버", "내 이름은?"]

for query in querys:
    response = history_chain.invoke(
        {"question": query},
        config={"configurable": {"session_id": session_id}}
    )
    print(response)