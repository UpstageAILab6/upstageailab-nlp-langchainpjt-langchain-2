from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import llm

# 세션 기록을 저장할 딕셔너리
store = {}


# 세션 ID를 기반으로 세션 기록을 가져오는 함수
def get_session_history(session_id):
    # print(f"[대화 세션ID]: {session_id}")
    
    if session_id not in store:  # 세션 ID가 store에 없는 경우
        # 새로운 ChatMessageHistory 객체를 생성하여 store에 저장
        store[session_id] = ChatMessageHistory()
    return store[session_id]  # 해당 세션 ID에 대한 세션 기록 반환

def get_chain_with_history(chain):
    # 세션 ID를 생성합니다.
    session_id = "session_1"  # 예시로 고정된 세션 ID 사용
    # 세션 기록을 가져옵니다.
    session_history = get_session_history(session_id)
    
    # LLM 체인을 생성합니다.
    llm = llm.get_model_chain()
    
    # 세션 기록을 포함한 체인 생성
    chain_with_history = RunnableWithMessageHistory(
        chain,
        session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
    
    return chain_with_history