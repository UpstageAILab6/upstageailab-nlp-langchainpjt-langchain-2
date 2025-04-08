[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/5BS4k7bR)
# **LangChain 프로젝트**

LangChain 기술을 활용하여, 노무 상담 QA봇 시스을 구축하는 프로젝트입니다.  
RAG(Retrieval-Augmented Generation) 구조를 바탕으로 문서 검색 및 응답 시스템을 구현하고, 전체 모델 생애주기를 관리 가능한 파이프라인으로 구성했습니다.

- **프로젝트 기간:** 2025. 04. 02 ~ 2025. 04. 08 
- **주제:** LangChain 기반 문서 검색 + Q&A 자동화 시스템  

---

# **팀원 소개**

| 이름      | 역할             | GitHub                | 담당 기능                                         |
|-----------|------------------|------------------------|--------------------------------------------------|
| **정준성** | 팀장 / PDFLoader 전처리 | [GitHub 링크](#)       | PDFLoader 성능비교, PDF 전처리 |
| **김지혜** |  사용성개선/git 관리   | [GitHub 링크](#)       | LangChain 통합, streamlit으로 환경개선 |
| **하선영** | 자료준비/Chunking | [GitHub 링크](#)       | 데이터 수집, Chunking 성능비교           |
| **최영진** | 대화기억/프롬프트     | [GitHub 링크](#)       | LLM 프롬프트, RAG 대화기억     |

---

# **파이프라인 워크플로우**

LangChain 기반 문서 QA 시스템의 구축 및 운영을 위한 파이프라인입니다.
1. PDFPlumberLoader를 통해 PDF 내용 Load
2. clean_text를 통해 전처리
3. RecursiveCharacterTextSplitter를 사용해 text_split
4. upstage embedding model을 통해 embedding
5. Faiss로 vector_store 구축
6. Faiss 기반 vector Retriever 사용
7. Retriever를 통해 context를 구성하고, Prompt와 함께 chat_history, question 등을 Chain 하여 Upstage solar-pro에게 전송
8. solar-pro의 응답

## **1. 비즈니스 문제 정의**
- 노무 문서에 대한 빠르고 정확한 자동 응답 시스템 구축

## **2. 데이터 수집 및 전처리**
1. **데이터 수집**
   - 2024년 노무관리 가이드, 고용노동부-2025년, 근로기준법
2. **문서 파싱 및 전처리**
   - LangChain의 DocumentLoader 사용
   - Chunking, Text Cleaning
3. **임베딩 및 벡터화**
   - U Embedding 모델 사용
   - FAISS을 활용한 vector_store 구축

## **3. LLM 및 RAG 파이프라인 구성**
- Faiss 기반 벡터 Retriever 모듈 활용
- Chain 구성: Embedding → Retriever → LLM(응답)
- LLM: Upstage Solar

## **4. 모델 학습 및 실험 추적**
- LangSmith를 사용해 실험 추적

## **5. 실행 환경 구성**
1. **Streamlit으로 웹 환경에서 실행**

---

## **프로젝트 실행 방법**

bash에서 streamlit run main.py를 입력해 실행

```bash
# 1. 프로젝트 클론
git clone https://github.com/UpstageAILab6/upstageailab-nlp-langchainpjt-langchain-2.git
cd upstageailab-nlp-langchainpjt-langchain-2

# 2. 가상환경 설정 및 패키지 설치
pip install -r requirements.txt

# 3. 환경 변수 설정
export API_KEY=your-api-key

# 4. 실행
streamlit run main.py
```

---

## **활용 장비 및 사용 툴**

### **활용 장비**
- **개발 환경:** \Python 3.10+
- **테스트 환경:** colab 서버
- 
### **협업 툴**
- **소스 관리:** GitHub
- **실험 관리:** LangSmith
- **커뮤니케이션:** Slack
- **버전 관리:** Git

---

## **기대 효과 및 향후 계획**
- 문서 기반 질문 응답 자동화로 고객 응대 시간 절감
- 노무 문서 검색 정확도 및 사용성 향상
- 향후 다양한 도메인 문서(QA, 정책, 교육자료 등)에 확장 적용 예정


