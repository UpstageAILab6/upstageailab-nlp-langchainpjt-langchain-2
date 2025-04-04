import chat_history

if __name__ == "__main__":
    # 실행할 질문
    question = "제 이름은 정준성입니다."

    # RAG 실행
    response = chat_history.chain_with_history.invoke(
        {"question": question},
        config={"configurable": {"session_id": "rag123"}},
    )

    print(response)