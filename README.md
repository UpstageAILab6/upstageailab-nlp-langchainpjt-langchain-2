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

## **강사님 피드백 및 프로젝트 회고**

프로젝트 진행 중 담당 강사님과의 피드백 세션을 통해 얻은 주요 인사이트는 다음과 같습니다.

### 📌 **1차 피드백 (2025.04.03)**
- **주제 선정**  
  → 도메인 분기 기반 Q&A라는 주제의 명확성 확보 및 활용도 고려
- **데이터 Chunking 전략**  
  → 텍스트의 의미 단위로 나누는 전략 필요성 제시
- **Embedding DB 구성 초기 설계**  
  → 단일 Vector Store가 아닌 도메인별 벡터 저장소 구성 제안

### 📌 **2차 피드백 (2025.04.04)**
- **Embedding DB 구성 고도화**  
  → 유연한 검색을 위한 필터링 및 메타데이터 설계 강조
- **실행 가능 코드 구성**  
  → 짧은 시간 내 프로토타입 수준의 실행 가능한 구조 완성 제안

### 📌 **3차 피드백 (2025.04.07)**
- **벡터 DB 다양화**  
  → FAISS 외에도 Qdrant, Milvus 등 비교 실험 제안
- **System Message Prompting**  
  → 프롬프트 설계 시 시스템 메시지를 활용해 문맥 유지 유도
- **Routing 전략 정교화**  
  → 질문의 도메인 분기를 좀 더 유연하게 처리하는 함수 설계 필요
- **응답 품질 요소 제안**  
  - **답변 길이 조절**: 질문 맥락에 맞는 길이로 최적화 필요  
  - **Ground Check 도입**: UpstageAI의 CAG 기반 평가 방법 참조  
    - [CAG_GC Notebook](https://github.com/UpstageAI/cookbook/blob/main/Solar-Fullstack-LLM-101/04_CAG_GC.ipynb) 활용 권장  
    - 실제 응답과 Ground Truth 비교를 통한 평가 체계 수립
