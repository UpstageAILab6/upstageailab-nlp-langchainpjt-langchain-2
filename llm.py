from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
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
        return PromptTemplate.from_template(
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

    def _create_chain(self):
        try:
            logger.info("Initializing LLM chain")
            llm = ChatUpstage(api_key=Config.API_KEY, model=Config.LLM_MODEL)
            prompt = self._create_prompt()
            return (
                {
                    "context": itemgetter("question") | self.retriever,
                    "question": itemgetter("question"),
                    "chat_history": itemgetter("chat_history"),
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