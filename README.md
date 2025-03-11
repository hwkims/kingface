![image](https://github.com/user-attachments/assets/1fd8eb0a-7306-495f-b043-cea822427560)
![image](https://github.com/user-attachments/assets/c1ffa583-c698-44a5-a82c-c365e5c8987c)

![image](https://github.com/user-attachments/assets/75323d5a-7225-40ea-bc98-40c517d8882d)

![image](https://github.com/user-attachments/assets/4467fd6f-6aaa-438f-91a2-381de6a3e2bf)

![image](https://github.com/user-attachments/assets/365e5a87-6663-40ea-8710-ceec8147e967)
![image](https://github.com/user-attachments/assets/b7cc629c-265d-4694-8fbb-10df173d1896)

![image](https://github.com/user-attachments/assets/1b9e7407-341c-4345-8160-0d04f4ec27ae)




```markdown
# AI 관상 서비스 (Ollama 기반)






[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/your-username/your-repo-name/blob/main/your-notebook-name.ipynb)  <!-- Colab 링크가 있다면 추가 -->

이 프로젝트는 Ollama와 Streamlit을 사용하여 얼굴 이미지를 분석하고 관상 정보를 제공하는 웹 애플리케이션입니다. 32가지 핵심 얼굴 특징을 기반으로 상세한 분석 결과를 제공합니다.

## ✨ 주요 기능

- **웹캠 연동:**  실시간으로 웹캠을 통해 사진을 찍고 분석할 수 있습니다.
- **파일 업로드:**  이미지 파일 (jpg, jpeg, png)을 업로드하여 분석할 수 있습니다.
- **상세 관상 분석:**
    - 나이, 성별, 인종 추정
    - 행복도, 근육 처짐 정도 (0-100%)
    - 직업 범주, 수입, 학력 추정
    - 32가지 얼굴 특징 상세 분석 (0-100%) 및 레이더 차트 시각화
    - 전반적인 인상 요약
- **Ollama 통합:**  `granite3.2-vision` 모델을 사용하여 이미지 분석을 수행합니다.
- **Streamlit UI:**  사용자 친화적인 인터랙티브 웹 인터페이스를 제공합니다.
- **에러 처리:** 웹캠 접근 오류, Ollama API 오류, JSON 파싱 오류 등을 처리합니다.

## 🛠️ 기술 스택

- **Python 3.7+**
- **Streamlit:** 웹 애플리케이션 프레임워크
- **Ollama:**  대규모 언어 모델 (LLM) 실행 및 관리
   -  `granite3.2-vision` 모델 사용 (얼굴 분석)
- **Requests:**  HTTP 요청 라이브러리
- **Pillow (PIL):**  이미지 처리 라이브러리
- **Base64:** 이미지 인코딩/디코딩
- **JSON:** 데이터 교환 형식
- **Regular Expressions (re):**  텍스트 패턴 매칭
- **Plotly:**  데이터 시각화 (레이더 차트)
- **HTML/CSS/JavaScript:** 웹캠 연동 및 UI 커스터마이징

## 💻 실행 방법

### 로컬 환경 (권장)

1. **Ollama 설치 및 실행:**
   - Ollama 공식 웹사이트에서 설치 가이드를 따라 설치합니다: [https://ollama.ai/](https://ollama.ai/)
   - Ollama를 실행하고 `granite3.2-vision` 모델을 pull 받습니다:
     ```bash
     ollama run granite3.2-vision
     ```
   - Ollama 서버가 `http://localhost:11434`에서 실행 중인지 확인합니다.

2. **저장소 복제:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git  # 실제 저장소 주소로 변경
   cd your-repo-name
   ```

3. **필수 패키지 설치:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Streamlit 앱 실행:**
   ```bash
   streamlit run app.py  # app.py는 실제 파일 이름
   ```
   웹 브라우저에서 앱이 자동으로 열립니다.

### Google Colab (선택 사항)

1. **Colab 노트북 열기:**  README 상단의 "Open In Colab" 배지를 클릭합니다.
2. **Ollama 설치 (Colab 환경):**
   ```python
   !curl https://ollama.ai/install.sh | sh
   ```
   ```python
    import subprocess
    # 백그라운드에서 Ollama 서버 시작 &
    subprocess.Popen(["ollama", "serve"])
   ```
3. **필수 패키지 설치:**
    ```python
    !pip install streamlit requests pillow plotly
    ```
4. **`app.py` 업로드**:  Colab 세션에 `app.py` 파일을 업로드합니다.

5.  **ngrok 설치 및 Streamlit 앱 실행 (Colab에서 외부 접근 허용):**

    ```python
    !pip install pyngrok
    ```

    ```python
    from pyngrok import ngrok

    # Streamlit 앱을 백그라운드에서 실행
    get_ipython().system_raw("streamlit run app.py &")

    # ngrok 터널 생성 (Streamlit 포트 8501)
    public_url = ngrok.connect(8501)
    print("Streamlit 앱에 접근할 수 있는 공개 URL:", public_url)
    ```
    출력된 ngrok URL을 통해 웹 브라우저에서 앱에 접근합니다.

## ⚠️ 주의 사항

- **웹캠 접근 권한:**  웹캠을 사용하는 경우 브라우저에서 웹캠 접근 권한을 허용해야 합니다.
- **Ollama 모델:** `granite3.2-vision` 모델이 Ollama에 설치되어 있어야 합니다.  `ollama run granite3.2-vision` 명령어로 설치할 수 있습니다.
- **시간 초과:**  Ollama API 호출 시 네트워크 상황에 따라 시간이 오래 걸릴 수 있습니다.  `timeout` 값을 적절히 조절하세요 (현재 120초).
- **개인정보:**  업로드하는 이미지에 민감한 개인정보가 포함되지 않도록 주의하세요. 이 서비스는 분석 목적으로만 이미지를 사용하며, 저장하지 않습니다.
- **정확도:**  AI 모델의 예측은 100% 정확하지 않을 수 있습니다.  결과는 참고용으로만 사용하세요.
- **Colab 제한:**  Colab 환경은 세션이 종료되면 모든 데이터가 초기화됩니다.  영구적인 사용을 위해서는 로컬 환경을 구축하는 것이 좋습니다.  Colab은 일시적인 테스트/데모 용도로 적합합니다.

## 🤝 기여

버그 수정, 기능 추가 등 어떤 형태의 기여도 환영합니다.  Pull Request를 통해 기여해주세요.

## 📄 라이선스

[MIT License](LICENSE)  <!-- 라이선스 파일이 있다면 링크 -->

## 📧 연락처

문의 사항이 있으면 [your.email@example.com](mailto:your.email@example.com)으로 연락주세요.  <!-- 실제 이메일 주소로 변경 -->
```

**주요 변경 사항:**

- **섹션 추가:**  "주요 기능", "기술 스택", "실행 방법" (로컬/Colab), "주의 사항", "기여", "라이선스", "연락처" 섹션을 추가하여 README의 완성도를 높였습니다.
- **Colab 실행 방법:**  Colab 환경에서 Ollama를 설치하고, ngrok을 사용하여 외부에서 접근 가능하도록 하는 방법을 상세히 설명했습니다.
- **배지 추가:**  "Open In Colab" 배지를 추가하여 사용자가 Colab 환경에서 바로 코드를 실행해 볼 수 있도록 했습니다. (Colab 노트북이 있다면)
- **명확한 설명:**  각 단계별로 자세하고 명확한 설명을 추가하여 사용자가 쉽게 따라 할 수 있도록 했습니다.
- **주의 사항 강조:**  웹캠 접근 권한, 모델 정확도, 개인정보, Colab 제한 사항 등 중요한 주의 사항을 강조했습니다.
- **마크다운 형식:**  가독성을 높이기 위해 마크다운 형식을 적극적으로 활용했습니다.
- **requirements.txt 언급:**  `pip install -r requirements.txt` 를 통해 필요한 패키지를 설치하도록 안내했습니다.
- **Ollama 설치 가이드 링크:** Ollama 공식 웹사이트 링크를 추가.
- **ngrok 사용법:** Colab환경에서 ngrok을 사용하는 방법을 추가.
- **Popen 사용:** Ollama 서버를 백그라운드에서 실행하도록 수정.
- **get_ipython().system_raw:** Streamlit을 백그라운드로 실행.

이 README는 템플릿입니다.  실제 프로젝트 정보 (GitHub 저장소 주소, 이메일 주소, Colab 노트북 링크, 라이선스 파일 등)를 반영하여 수정해야 합니다.
