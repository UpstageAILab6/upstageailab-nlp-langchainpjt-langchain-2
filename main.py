import chat_history
<<<<<<< HEAD

if __name__ == "__main__":
    while True:
        # 실행할 질문
        question = input("입력: ")

        # RAG 실행
        response = chat_history.chain_with_history.invoke(
            {"question": question},
            config={"configurable": {"session_id": "rag123"}},
        )

        print(response)
=======
import llm
import vector_store
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    # PDF 파일 경로
    # TODO: add data to gitignore
    # pdf_file_path = "./data/★ 2024 노무관리 가이드 북.pdf"
    pdf_file_path = "./data/근로기준법(법률)(제20520호)(20250223).pdf"

    # 벡터스토어 생성
    vectorstore = vector_store.get_vectorstore(pdf_file_path)

    retriever = vectorstore.as_retriever()

    chain = llm.get_model_chain(retriever)

    # 질문 및 대화 이력 초기화
    question = "퇴직금은 1년 미만 근무해도 받을 수 있나요?"

    # 질문에 대한 답변 생성
    answer = chain.invoke(question)
    
    # 답변 출력
    print(answer)
    
if __name__ == "__main__":
    main()
    
>>>>>>> bfe289e (add function base code)
