import streamlit as st
import requests
import base64
import json
import re
from PIL import Image
import io
import streamlit.components.v1 as components
import plotly.graph_objects as go
import random  # random import 추가


# Ollama 서버 주소
OLLAMA_HOST = 'http://localhost:11434'

def query_ollama(prompt, image_data):
    """Ollama API 호출"""
    data = {
        "model": "granite3.2-vision",
        "prompt": prompt,
        "stream": False,
        "images": [image_data],  # base64 문자열
        "options": {"temperature": 0} # 0으로 유지 (결정적)
    }
    response = requests.post(f"{OLLAMA_HOST}/api/generate", json=data, timeout=120)
    response.raise_for_status()
    return response.json()

def parse_ollama_response(response_text):
    """Ollama 응답 파싱"""
    try:
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            return json.loads(json_str)
        else:
            return {"error": "No valid JSON"}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {e}"}

def generate_prompt():
    """JSON 형식 프롬프트 생성 (추가 정보 포함)"""
    prompt = """
    Analyze the face and provide a detailed physiognomy reading in JSON format. The output *MUST* be valid JSON, and *MUST* strictly adhere to the following structure:

    ```json
    {
      "age": (integer, estimated age),
      "gender": (integer, 0 for female, 1 for male, 2 for non-binary/uncertain),
      "ethnicity": (integer, 0: East Asian, 1: Caucasian, 2: African, 3: South Asian, 4: Hispanic, 5: Middle Eastern, 6: Southeast Asian, 7: Native American, 8: Pacific Islander, 9: Other),
      "happiness": (integer, 0-100, 0 is very unhappy, 100 is very happy),
      "muscle_sagging": (integer, 0-100, 0 is no sagging, 100 is severe sagging),
      "features": {
        "forehead_height": (integer, 0-100),
        "forehead_width": (integer, 0-100),
        "eyebrow_distance": (integer, 0-100),
        "eyebrow_thickness": (integer, 0-100),
        "eyebrow_arch": (integer, 0-100),
        "eye_size": (integer, 0-100),
        "eye_distance": (integer, 0-100),
        "eye_slant": (integer, 0-100),
        "eyelid_fold": (integer, 0-100),
        "under_eye_bags": (integer, 0-100),
        "nose_length": (integer, 0-100),
        "nose_width": (integer, 0-100),
        "nose_tip_angle": (integer, 0-100),
        "nostril_size": (integer, 0-100),
        "philtrum_length": (integer, 0-100),
        "lip_fullness_upper": (integer, 0-100),
        "lip_fullness_lower": (integer, 0-100),
        "mouth_width": (integer, 0-100),
        "chin_size": (integer, 0-100),
        "chin_projection": (integer, 0-100),
        "jawline_strength": (integer, 0-100),
        "cheekbone_prominence": (integer, 0-100),
        "cheek_fullness": (integer, 0-100),
        "temple_width": (integer, 0-100),
        "face_length": (integer, 0-100),
        "face_width": (integer, 0-100),
        "skin_smoothness": (integer, 0-100),
        "wrinkle_forehead": (integer, 0-100),
        "wrinkle_eyes": (integer, 0-100),
        "nasolabial_fold_depth": (integer, 0-100),
        "hairline_recession": (integer, 0-100),
        "ear_size": (integer, 0-100)
      },
      "occupation_category": (integer, 0: creative, 1: business, 2: science/tech, 3: education, 4: healthcare, 5: service, 6: other),
      "income": (integer, 0-100, 0 is low, 100 is high),
      "education": (integer, 0: no college, 1: some college, 2: bachelor's, 3: master's, 4: doctoral),
      "overall_impression": (string, concise summary),
      "recommended_name": {
          "last_name": (string),
          "first_name": (string)
      },
      "lotto_winning_chance": (integer, 0-100),
      "mbti": (string, 4-letter MBTI code),
      "blood_type": (string, e.g., "A", "B", "AB", "O"),
      "zodiac_sign": (string, e.g., "Aries", "Taurus", etc.)
    }
    ```

    All values except for "overall_impression", names, MBTI, blood type and zodiac sign MUST be integers. The "features" object MUST contain exactly the 32 named facial features as keys.  Values for features should be between 0 and 100.  Be specific and concise. Do NOT include explanations.
    """
    return prompt


def plot_features(features):
    """얼굴 특징 레이더 차트"""
    categories = list(features.keys())
    values = list(features.values())
    categories = categories + [categories[0]]
    values = values + [values[0]]
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="얼굴 특징 분석"
    )
    return fig

def display_results(result):
    """결과 표시 (업데이트)"""
    st.subheader("관상 결과")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("나이", result.get('age', 'N/A'))
    with col2:
        st.metric("성별", "여성" if result.get('gender') == 0 else "남성" if result.get('gender') == 1 else "N/A")
    with col3:
         st.metric("인종", {0: "동아시아", 1: "백인", 2: "아프리카", 3: "남아시아", 4: "히스패닉", 5: "중동", 6: "동남아시아", 7: "아메리카 원주민", 8: "태평양 섬", 9: "기타"}.get(result.get('ethnicity'), 'N/A'))
    with col4:
        st.metric("행복도", f"{result.get('happiness', 'N/A')}%")

    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("근육 처짐", f"{result.get('muscle_sagging', 'N/A')}%")
    with col6:
        st.metric("직업 범주", {0: "창의", 1: "비즈니스", 2: "과학/기술", 3: "교육", 4: "의료", 5: "서비스", 6: "기타"}.get(result.get('occupation_category'), 'N/A'))
    with col7:
        st.metric("수입", f"{result.get('income','N/A')}%")

    features = result.get('features', {})
    if features:
        fig = plot_features(features)
        st.plotly_chart(fig)
    else:
        st.write("얼굴 특징 데이터가 없습니다.")

    # 추가 정보 (한국인이 좋아하는 요소)
    st.subheader("추가 분석")

    # 왕이 될 상 (이전 코드 유지)
    king_score = 0
    if features:
      king_score += features.get("forehead_width", 0) * 0.2
      king_score += features.get("forehead_height", 0) * 0.2
      king_score += features.get("eyebrow_thickness",0) * 0.15
      king_score += (100 - abs(features.get("eyebrow_distance", 50) - 50)) * 0.1
      king_score += features.get("jawline_strength", 0) * 0.2
      king_score += features.get("chin_projection", 0) * 0.15
    st.metric("왕이 될 상", f"{king_score:.1f}%")

    # 추천 이름 (AI 생성)
    recommended_name = result.get("recommended_name", {})
    last_name = recommended_name.get("last_name", "N/A")
    first_name = recommended_name.get("first_name", "N/A")
    st.write(f"**추천 이름:** {last_name}{first_name}")


    # 연예인 가능성 (이전 코드 유지)
    celebrity_score = 0
    if features:
        symmetry_score = 0
        symmetry_score += (100 - abs(features.get("eye_size", 50) - 50)) * 0.2
        symmetry_score += (100 - abs(features.get('cheekbone_prominence',50)-50)) * 0.1
        symmetry_score += (100- abs(features.get('cheek_fullness',50)-50)) *0.1
        celebrity_score += symmetry_score * 0.4
        celebrity_score += features.get("skin_smoothness", 0) * 0.3
        celebrity_score += (100 - features.get("wrinkle_forehead", 0)) * 0.05
        celebrity_score += (100 - features.get("wrinkle_eyes", 0)) * 0.05
        celebrity_score += features.get("eye_size", 0) * 0.1
        celebrity_score += (100- features.get('under_eye_bags',0)) * 0.1
    st.metric("연예인 가능성", f"{celebrity_score:.1f}%")

    # 운 (이전 코드 유지 + 로또 당첨 확률)
    luck_score = result.get("happiness", 0) * 0.6
    if "긍정적" in result.get("overall_impression", ""):
        luck_score += 20
    elif "부정적" in result.get("overall_impression",""):
        luck_score -=10
    st.metric("운", f"{luck_score:.1f}%")

    st.metric("로또 당첨 확률", f"{result.get('lotto_winning_chance', 'N/A')}%")  # 로또 확률
    st.write(f"**MBTI:** {result.get('mbti', 'N/A')}")  # MBTI
    st.write(f"**혈액형:** {result.get('blood_type', 'N/A')}")  # 혈액형
    st.write(f"**별자리:** {result.get('zodiac_sign', 'N/A')}") # 별자리

    st.write(f"**전반적인 인상:** {result.get('overall_impression', 'N/A')}")

def main():
    st.title("AI 관상 서비스 (Ollama)")
    st.write("32가지 핵심 얼굴 특징을 기반으로 관상을 분석합니다.")

    # 옵션 선택: 웹캠 또는 파일 업로드
    option = st.radio("이미지 소스 선택:", ("웹캠", "파일 업로드"), horizontal=True)

    if option == "웹캠":
        # 웹캠 (JavaScript) + 사진 찍기 버튼 (HTML, CSS, JavaScript)
        components.html(
            """
            <style>
            /* 버튼 스타일 */
            #capture {
                background-color: #4CAF50; /* 녹색 */
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px; /* 둥근 모서리 */
            }
            /* 마우스 오버 효과 */
            #capture:hover {
                background-color: #45a049;
            }

            /* 비디오 크기 및 위치 조정 */
            #video-container {
                position: relative; /* 상대 위치 */
                width: 320px;
                height: 240px;
            }

            #video {
                width: 100%; /* 컨테이너에 맞게 조정 */
                height: 100%;
                object-fit: cover; /* 비율 유지하며 채우기 */
            }
            #capture-container{
                text-align: center; /* 버튼 가운데 정렬 */
            }


            </style>
            <div id="video-container">
                <video id="video" autoplay></video>
            </div>
            <div id="capture-container">
                <button id="capture">사진 찍기</button>
            </div>
            <canvas id="canvas" width="320" height="240" style="display:none;"></canvas>
            <script>
                const video = document.getElementById('video');
                const canvas = document.getElementById('canvas');
                const captureButton = document.getElementById('capture');
                const context = canvas.getContext('2d');

                // 웹캠 접근
                navigator.mediaDevices.getUserMedia({ video: true })
                    .then(stream => {
                        video.srcObject = stream;
                    })
                    .catch(err => {
                        console.error("Error accessing webcam:", err);
                        const errorEvent = new CustomEvent('webcamError', {detail: err.message});
                        document.dispatchEvent(errorEvent);
                    });

                // 사진 찍기 버튼 클릭 이벤트
                captureButton.addEventListener('click', () => {
                    context.drawImage(video, 0, 0, canvas.width, canvas.height); // 비디오 프레임을 캔버스에 그림
                    const imageData = canvas.toDataURL('image/jpeg').split(',')[1]; // base64로 인코딩

                    // Python으로 데이터 전송 (CustomEvent 사용)
                    const event = new CustomEvent('capturedImage', {detail: imageData});
                    document.dispatchEvent(event);

                    // Streamlit UI 업데이트를 위해 약간의 지연 (임시)
                    // setTimeout(() => {  //<- 이부분 주석처리
                    //     const updateEvent = new CustomEvent('updateUI');
                    //     document.dispatchEvent(updateEvent);
                    // }, 500); // 500ms 지연 (적절히 조절)


                });
            </script>
            """,
            height=350,  # 버튼 표시, 적절한 높이
        )

        # 이벤트 리스너 (JS -> Python, session_state 사용)
        image_data_js = components.html( #반환값을 image_data_js 에 저장
            """
            <script>
            // capturedImage 이벤트 리스너
            document.addEventListener('capturedImage', (e) => {
                console.log("capturedImage 이벤트 발생:", e.detail);
                // session_state에 저장 -> Python에서 사용
                window.parent.Streamlit.setSessionState({captured_image: e.detail});


            });
            // webcamError 이벤트 리스너
            document.addEventListener('webcamError', (e) => {
                console.log("webcamError 이벤트 발생:", e.detail);
                 // session_state에 에러 저장 -> Python에서 사용
                window.parent.Streamlit.setSessionState({webcam_error: 'Error: ' + e.detail});
            });


            </script>""", height=0)


        # session_state에서 데이터 가져오기 + None 처리
        captured_image_data = st.session_state.get('captured_image')
        webcam_error = st.session_state.get('webcam_error')

        if webcam_error:  # 웹캠 에러 처리
            st.error(webcam_error)
            st.session_state['webcam_error'] = None #에러메시지 표시 후, 초기화

        elif captured_image_data: #캡처된 이미지가 있으면.
            try:
                # base64 디코딩
                img_bytes = base64.b64decode(captured_image_data)
                # 이미지 표시
                img = Image.open(io.BytesIO(img_bytes))
                st.image(img, caption="캡처된 이미지", use_column_width=True)

                # 분석 (spinner 사용)
                with st.spinner("분석 중..."):
                    prompt = generate_prompt()
                    # base64 인코딩된 데이터를 그대로 Ollama에 전송
                    ollama_response = query_ollama(prompt, captured_image_data)

                    if "error" in ollama_response:
                        st.error("Ollama 오류: " + ollama_response["error"])
                        if "raw_response" in ollama_response: # 원시 응답 (있는경우)
                            st.write("Ollama 원시 응답:")
                            st.text(ollama_response["raw_response"]) #text로.
                    else:
                        result = parse_ollama_response(ollama_response['response'])
                        if "error" in result: # 파싱 에러
                            st.error("JSON 파싱 오류: " + result["error"])
                        else: # 정상
                            display_results(result)  # 결과 표시

                # 이미지 처리 후, session_state에서 제거 (다음 캡처를 위해)
                st.session_state['captured_image'] = None # 세션에서 제거

            except Exception as e:
                st.error(f"이미지 처리 오류: {e}")


    elif option == "파일 업로드":
        uploaded_file = st.file_uploader("얼굴 이미지를 업로드하세요.", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="업로드된 이미지", use_column_width=True)
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            if st.button("관상 분석"):
                with st.spinner("분석 중..."):
                    prompt = generate_prompt()
                    ollama_response = query_ollama(prompt, img_str)
                    if "error" in ollama_response:
                        st.error("오류: " + ollama_response["error"])
                        if "raw_response" in ollama_response:
                            st.write("Ollama 원시 응답:")
                            st.text(ollama_response["raw_response"])
                    else:
                        result = parse_ollama_response(ollama_response['response'])
                        if "error" in result:
                            st.error("JSON 파싱 오류: " + result["error"])
                        else:
                            display_results(result)

if __name__ == "__main__":
    main()
