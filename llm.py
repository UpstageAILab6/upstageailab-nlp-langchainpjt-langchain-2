from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_upstage import ChatUpstage
from operator import itemgetter
import logging
from config import Config
from retriever import Retriever

# 로깅 설정
logger = logging.getLogger(__name__)

class LLMChain:
    
    def __init__(self, retriever: Retriever):
        self.retriever = retriever.get_retriever()
        self.chain = self._create_chain()

    def _create_prompt(self) -> PromptTemplate:
        logger.info("Creating prompt template")
        return PromptTemplate.from_template("""
당신은 고도로 지능적인 QA 엔진입니다. 제공된 문서 참조 내용과 이전 대화 내용을 바탕으로 사용자의 질문에 답변하세요. 답변은 다음 지침을 따르세요:
1. 문서 참조 내용과 이전 대화 내용을 우선적으로 활용해 정확한 답변을 제공.
2. 문서나 대화에 정보가 부족하면, 일반 지식을 사용해 보완하되 출처가 다름을 명시.
3. 간결하고 명확하게 답변하며, 필요 시 간단한 설명 추가.

문서 참조 내용:
{context}

이전 대화 내용:
{chat_history}

질문:
{question}
"""
        )
    
    def _get_formatted_history(self, messages):
        result = []
        for idx in range(0, len(messages), 2):
            result.append((f"USER: {messages[idx].content}", f"AI: {messages[idx+1].content}"))
        return result

    def _create_chain(self):
        try:
            logger.info("Initializing LLM chain")
            llm = ChatUpstage(api_key=Config.API_KEY, model=Config.LLM_MODEL)
            prompt = self._create_prompt()
            return (
                {
                    "context": itemgetter("question") | self.retriever | (lambda x: "\n".join(doc.page_content for doc in x)),
                    "chat_history": itemgetter("chat_history") | RunnableLambda(self._get_formatted_history),
                    "question": itemgetter("question"),
                }
                | prompt
                | llm
                | StrOutputParser()
            )
        except Exception as e:
            logger.error(f"Failed to create LLM chain: {str(e)}")
            raise

    def get_chain(self):
        return self.chain

__all__ = ["LLMChain"]
