from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import logging
from llm import LLMChain
from config import Config

# 로깅 설정
logger = logging.getLogger(__name__)

class LimitedChatMessageHistory(ChatMessageHistory):
    def add_message(self, message):
        super().add_message(message)
        if len(self.messages) > 10:  # 최대 10개 메시지 유지
            self.messages = self.messages[-10:]

class ChatHistoryManager:
    def __init__(self, llm_chain: LLMChain):
        self.store = {}
        self.chain_with_history = self._create_chain_with_history(llm_chain)

    def _get_session_history(self, session_id: str) -> LimitedChatMessageHistory:
        if session_id not in self.store:
            logger.info(f"Creating new chat history for session: {session_id}")
            self.store[session_id] = LimitedChatMessageHistory()
        return self.store[session_id]

    def _create_chain_with_history(self, llm_chain: LLMChain):
        try:
            logger.info("Creating chain with chat history")
            return RunnableWithMessageHistory(
                llm_chain.get_chain(),
                self._get_session_history,
                input_messages_key="question",
                history_messages_key="chat_history",
            )
        except Exception as e:
            logger.error(f"Failed to create chain with history: {str(e)}")
            raise

    def get_chain(self):
        return self.chain_with_history

    def clear_history(self, session_id: str):
        if session_id in self.store:
            logger.info(f"Clearing chat history for session: {session_id}")
            del self.store[session_id]

__all__ = ["ChatHistoryManager"]