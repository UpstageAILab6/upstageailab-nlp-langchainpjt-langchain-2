from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_upstage import ChatUpstage
<<<<<<< HEAD
from operator import itemgetter
from dotenv import load_dotenv
import os
import retriever
from chat_history import *

# API 키 정보 로드
load_dotenv()

# 단계 6: 프롬프트 생성(Create Prompt)
=======
from langchain_core.runnables import RunnablePassthrough
import utils
import retriever
from chat_history import *

>>>>>>> bfe289e (add function base code)
# 프롬프트를 생성합니다.
prompt = PromptTemplate.from_template(
    """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Answer in Korean.

<<<<<<< HEAD
#Previous Chat History:
{chat_history}

=======
>>>>>>> bfe289e (add function base code)
#Question:
{question}
#Context:
{context}

#Answer:"""
)

<<<<<<< HEAD
# 단계 7: 언어모델(LLM) 생성
# 모델(LLM) 을 생성합니다.
llm = ChatUpstage(api_key=os.getenv('API_KEY'), model="solar-pro")

# 단계 8: 체인(Chain) 생성
chain = (
    {
        "context": itemgetter("question") | retriever.retriever,
        "question": itemgetter("question"),
        "chat_history": itemgetter("chat_history"),
    }
    | prompt
    | llm
    | StrOutputParser()
)

__all__ = ["chain"]
=======
def get_model_chain(retriever):
    # 단계 7: 언어모델(LLM) 생성
    # 모델(LLM) 을 생성합니다.
    llm = ChatUpstage(api_key=utils.load_api_key(), model="solar-pro")

    # 단계 8: 체인(Chain) 생성
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
>>>>>>> bfe289e (add function base code)
