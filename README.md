![image](https://github.com/user-attachments/assets/1fd8eb0a-7306-495f-b043-cea822427560)
![image](https://github.com/user-attachments/assets/c1ffa583-c698-44a5-a82c-c365e5c8987c)

![image](https://github.com/user-attachments/assets/75323d5a-7225-40ea-bc98-40c517d8882d)

![image](https://github.com/user-attachments/assets/4467fd6f-6aaa-438f-91a2-381de6a3e2bf)

![image](https://github.com/user-attachments/assets/365e5a87-6663-40ea-8710-ceec8147e967)
![image](https://github.com/user-attachments/assets/b7cc629c-265d-4694-8fbb-10df173d1896)

![image](https://github.com/user-attachments/assets/1b9e7407-341c-4345-8160-0d04f4ec27ae)




# 👑 KingFace: AI 관상 분석 애플리케이션 (Ollama 기반)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hwkims/kingface/blob/main/app.py)  
**2024년 3월 12일 업데이트:** Gemma 모델 지원 추가!

이 프로젝트는 Ollama와 Streamlit을 사용하여 얼굴 이미지를 분석하고 관상 정보를 제공하는 웹 애플리케이션입니다.  32가지 핵심 얼굴 특징을 기반으로 상세한 분석 결과를 제공합니다.

## ✨ 주요 기능

- **웹캠 연동:** 실시간으로 웹캠을 통해 사진을 찍고 분석할 수 있습니다.
- **파일 업로드:** 이미지 파일 (jpg, jpeg, png)을 업로드하여 분석할 수 있습니다.
- **상세 관상 분석:**
    - 나이, 성별, 인종 추정
    - 행복도, 근육 처짐 정도 (0-100%)
    - 직업 범주, 수입, 학력 추정
    - 32가지 얼굴 특징 상세 분석 (0-100%) 및 레이더 차트 시각화
    - 전반적인 인상 요약
    - 추천 이름, MBTI, 혈액형, 별자리
    - 왕이 될 상, 연예인 가능성, 운, 로또 당첨 확률(!)
- **Ollama 통합:**
    - `gemma3:4b` 모델 (새롭게 추가됨!) 또는 `granite3.2-vision` 모델을 사용하여 이미지 분석을 수행합니다.  (모델 선택은 `app.py` 코드 내에서 이루어집니다.)
- **Streamlit UI:** 사용자 친화적인 인터랙티브 웹 인터페이스를 제공합니다.
- **에러 처리:** 웹캠 접근 오류, Ollama API 오류, JSON 파싱 오류 등을 처리합니다.

## 🛠️ 기술 스택

- **Python 3.7+**
- **Streamlit:** 웹 애플리케이션 프레임워크
- **Ollama:** 대규모 언어 모델 (LLM) 실행 및 관리
    - `gemma3:4b` 또는 `granite3.2-vision` 모델 사용 (얼굴 분석)
- **Requests:** HTTP 요청 라이브러리
- **Pillow (PIL):** 이미지 처리 라이브러리
- **Base64:** 이미지 인코딩/디코딩
- **JSON:** 데이터 교환 형식
- **Regular Expressions (re):** 텍스트 패턴 매칭
- **Plotly:** 데이터 시각화 (레이더 차트)
- **HTML/CSS/JavaScript:** 웹캠 연동 및 UI 커스터마이징
- **random**: 난수 생성 (로또 번호 추첨 😉)

## 💻 실행 방법 (로컬 환경)

1.  **Ollama 설치 및 실행:**
    -   Ollama 공식 웹사이트에서 설치 가이드를 따라 설치합니다: [https://ollama.ai/](https://ollama.ai/)
    -   Ollama를 실행하고 `gemma3:4b` 또는 `granite3.2-vision` 모델을 pull 받습니다:
        ```bash
        ollama pull gemma3:4b  # 또는 ollama pull granite3.2-vision
        ollama serve #Ollama 서버 실행
        ```
     - Ollama 서버가 `http://localhost:11434`에서 실행 중인지 확인합니다.

2.  **저장소 복제:**
    ```bash
    git clone https://github.com/hwkims/kingface.git
    cd kingface
    ```

3.  **필수 패키지 설치:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Streamlit 앱 실행:**
    ```bash
    streamlit run app.py
    ```
    웹 브라우저에서 앱이 자동으로 열립니다. (또는 안내되는 로컬 주소로 접속합니다.)

## ⚠️ 주의 사항

-   **웹캠 접근 권한:** 웹캠을 사용하는 경우 브라우저에서 웹캠 접근 권한을 허용해야 합니다.
-   **Ollama 모델:** `gemma3:4b` 또는 `granite3.2-vision` 모델 중 하나가 Ollama에 설치되어 있어야 합니다. `ollama pull <model_name>` 명령어로 설치할 수 있습니다.  `app.py` 코드 내에서 사용할 모델을 `gemma3:4b`로 지정하고 있습니다.  다른 모델을 사용하려면 해당 부분을 수정하세요.
-   **시간 초과:** Ollama API 호출 시 네트워크 상황에 따라 시간이 오래 걸릴 수 있습니다. `timeout` 값을 적절히 조절하세요 (현재 120초).
-   **개인정보:** 업로드하는 이미지에 민감한 개인정보가 포함되지 않도록 주의하세요. 이 서비스는 분석 목적으로만 이미지를 사용하며, 저장하지 않습니다.
-   **정확도:** AI 모델의 예측은 100% 정확하지 않을 수 있습니다. 결과는 참고용으로만 사용하세요.

## 🤝 기여

버그 수정, 기능 추가 등 어떤 형태의 기여도 환영합니다. Pull Request를 통해 기여해주세요.

## 📄 라이선스

MIT License
