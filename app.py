import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("⚾ MLB 상세 데이터 대시보드")

col_ui, col_data = st.columns([1, 3])

with col_ui:
    st.subheader("데이터 컨트롤")
    run_btn = st.button("데이터 새로고침")

with col_data:
    st.subheader("데이터 대시보드")
    data_placeholder = st.empty()

if run_btn:
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    params = {"playerID": "592450"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json().get('body', {})
            
            # [강제 평탄화 로직]
            # 데이터를 딕셔너리 리스트로 변환하여 표로 강제 변환
            # json_normalize는 중첩된 데이터를 표 형태로 펼쳐줍니다.
            df = pd.json_normalize(data)
            
            # 데이터프레임이 비어있지 않은지 확인
            if not df.empty:
                data_placeholder.dataframe(df, use_container_width=True)
            else:
                data_placeholder.warning("데이터가 비어있습니다.")
        else:
            data_placeholder.error(f"API 오류: {response.status_code}")
    except Exception as e:
        data_placeholder.error(f"오류: {e}")
