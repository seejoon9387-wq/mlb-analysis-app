import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("⚾ MLB 데이터 대시보드")

col_ui, col_data = st.columns([1, 3])

with col_ui:
    st.subheader("데이터 컨트롤")
    run_btn = st.button("데이터 새로고침")

with col_data:
    st.subheader("실시간 배당/데이터 대시보드")
    data_placeholder = st.empty()

if run_btn:
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    params = {"playerID": "592450"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            raw_json = response.json()
            body_data = raw_json.get('body', {})
            
            # [핵심] JSON을 평탄화하여 표로 변환
            # opponents 데이터가 리스트 형태라면 바로 DataFrame으로 변환
            if isinstance(body_data, dict) and 'opponents' in body_data:
                df = pd.DataFrame(body_data['opponents'])
                data_placeholder.dataframe(df, use_container_width=True)
            else:
                data_placeholder.write(f"데이터 형식이 표로 변환하기 어렵습니다: {body_data}")
        else:
            data_placeholder.error(f"API 오류: {response.status_code}")
    except Exception as e:
        data_placeholder.error(f"연결 오류: {e}")
