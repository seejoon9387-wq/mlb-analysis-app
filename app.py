import streamlit as st
import pandas as pd
import requests

# 페이지 구성
st.set_page_config(layout="wide")
st.title("⚾ MLB 데이터 디버깅 센터")

# [API 설정]
API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
HOST = "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
HEADERS = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST, "Content-Type": "application/json"}

# [데이터 호출 함수]
def fetch_debug_data():
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": "592450"} # 일단 고정 ID로 테스트
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            return response.json() # 결과 반환
        else:
            return f"에러코드: {response.status_code}"
    except Exception as e:
        return str(e)

# [UI 영역]
st.subheader("데이터 수신 상태 확인")
if st.button("데이터 강제 호출 및 확인"):
    raw_data = fetch_debug_data()
    
    # 1. 원본 데이터 출력 (이게 보여야 뭐가 문제인지 압니다)
    st.write("### 원본 응답 데이터:")
    st.json(raw_data) 
    
    # 2. 데이터 구조 파싱 시도
    try:
        if isinstance(raw_data, dict) and 'body' in raw_data:
            st.success("데이터 파싱 성공!")
            st.dataframe(pd.DataFrame([raw_data['body']]))
        else:
            st.warning("데이터가 비어있거나 구조가 'body'를 포함하지 않습니다.")
    except Exception as e:
        st.error(f"파싱 오류: {e}")
