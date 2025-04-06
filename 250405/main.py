import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_upstage import ChatUpstage, UpstageEmbeddings
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
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

# 프롬프트 정의
prompt = PromptTemplate(
    input_variables=["context", "history", "question"],
    template= "대화 기록:\n{history}\n문서: {context}\n질문: {question}\n답변:"
)

# query = "블랙핑크"

# context_docs = retriever.invoke(query)
# context = "\n".join([doc.page_content for doc in context_docs])

# question = query

# input_data = {
#     "context": context,
#     "question": question
# }

# formatted_prompt = prompt.format(**input_data)
# formatted_prompt = prompt.format(context=context, question=question)

# print(formatted_prompt)

def format_history(history):
    formatted = []
    for msg in history:
        role = "USER" if "HumanMessage" in str(type(msg)) else "AI"
        formatted.append(f"{role}: {msg.content}")
    return "\n".join(formatted)

base_chain =(
    # RunnableLambda(lambda x: {
    #     "context": "\n".join(doc.page_content for doc in retriever.invoke(x["question"])),
    #     "question": x["question"],
    #     "history": x.get("history", [])
    # })
    {
        "context": itemgetter("question") | retriever | (lambda x: "\n".join(doc.page_content for doc in x)),
        "question": itemgetter("question"),
        "history": itemgetter("history") | RunnableLambda(format_history)
    }
    | prompt
    | RunnableLambda(lambda x: print(x) or x)
    | llm
    | StrOutputParser()
)


# 메모리 저장소
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


chain_with_history = RunnableWithMessageHistory(
    runnable=base_chain,
    get_session_history=get_session_history,
    input_messages_key="question",
    history_messages_key="history"
)

while True:
    question = input("입력: ")
    response = chain_with_history.invoke(
        input= {"question": question},
        config={"configurable": {"session_id": "shayoyou"}}
    )
    print(response)
