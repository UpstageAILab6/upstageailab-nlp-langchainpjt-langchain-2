"""
Streamlit application for the Labor Management Chatbot.
Provides a user-friendly interface for interacting with the chatbot.
"""
import streamlit as st
import logging
from config import Config
from vector_store import VectorStoreManager
from retriever import Retriever
from llm import LLMChain
from chat_history import ChatHistoryManager

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatBot:
    """Core chatbot logic integrating all components."""
    
    def __init__(self, vector_store: VectorStoreManager, retriever: Retriever, 
                 llm_chain: LLMChain, chat_manager: ChatHistoryManager):
        self.chain = chat_manager.get_chain()
        self.chat_manager = chat_manager
        self.logger = logger

    def get_response(self, question: str) -> str:
        try:
            self.logger.info(f"Processing question: {question}")
            response = self.chain.invoke(
                {"question": question},
                config={"configurable": {"session_id": Config.SESSION_ID}},
            )
            return response
        except Exception as e:
            self.logger.error(f"Error processing question: {str(e)}")
            return "죄송합니다, 오류가 발생했습니다. 다시 시도해주세요."

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(page_title="노무관리 챗봇", layout="wide", initial_sidebar_state="collapsed")
    
    # 제목과 초기화 버튼을 상단에 배치
    col1, col2 = st.columns([8, 2])
    with col1:
        st.title("노무관리 챗봇")
        st.markdown("2024 노무관리 가이드 북을 기반으로 한 질문-답변 서비스입니다.")
    with col2:
        if st.button("대화 초기화", key="reset_chat"):
            st.session_state.messages = []
            st.session_state.chatbot.chat_manager.clear_history(Config.SESSION_ID)
            st.rerun()

    # 챗봇 초기화 (한 번만)
    if "chatbot" not in st.session_state:
        try:
            logger.info("Initializing chatbot components")
            Config.validate()
            vector_store = VectorStoreManager()
            retriever = Retriever(vector_store)
            llm_chain = LLMChain(retriever)
            chat_manager = ChatHistoryManager(llm_chain)
            st.session_state.chatbot = ChatBot(vector_store, retriever, llm_chain, chat_manager)
        except Exception as e:
            st.error(f"챗봇 초기화 실패: {str(e)}")
            logger.error(f"Chatbot initialization failed: {str(e)}")
            return
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 대화 기록 표시
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # 입력창
    prompt = st.chat_input("질문을 입력하세요:")
    if prompt:
        # 사용자 질문 추가 및 최대 10개 유지
        st.session_state.messages.append({"role": "user", "content": prompt})
        if len(st.session_state.messages) > 10:  # 5번 질의 응답 = 10개 메시지
            st.session_state.messages = st.session_state.messages[-10:]
        
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("답변 생성 중..."):
                    response = st.session_state.chatbot.get_response(prompt)
                st.markdown(response)
        
        # 챗봇 답변 추가 및 최대 10개 유지
        st.session_state.messages.append({"role": "assistant", "content": response})
        if len(st.session_state.messages) > 10:
            st.session_state.messages = st.session_state.messages[-10:]

if __name__ == "__main__":
    main()
