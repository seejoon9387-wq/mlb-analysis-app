import streamlit as st
import pandas as pd
import requests

# 페이지 레이아웃 고정
st.set_page_config(page_title="MLB AI Analyst", layout="wide")

# API 설정 (주신 정보 적용)
API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
HOST = "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"

# 헤더 설정
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": HOST,
    "Content-Type": "application/json"
}

st.title("⚾ MLB AI 분석 시스템")

# [상단 레이아웃] 항상 고정
c1, c2 = st.columns(2)
target_date = c1.date_input("분석 날짜")
days_range = c2.slider("분석 범위", 1, 30, 7)
st.divider()

# [좌우 분할] 항상 고정
col_left, col_right = st.columns([1.5, 2.5])

with col_left:
    st.subheader("📊 분석 엔진")
    st.text_input("선수 ID (예: 592450)")
    if st.button("선수 상세 분석"):
        st.success("데이터 호출 중...")

with col_right:
    st.subheader("⚡ 실시간 데이터 대시보드")
    
    # 선수 상세 데이터 호출
    def get_player_data(player_id="592450"):
        url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
        params = {"playerID": player_id}
        try:
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # 데이터가 존재할 경우 테이블로 변환
                if 'body' in data:
                    return pd.DataFrame([data['body']])
                return None
            else:
                return f"에러: {response.status_code}"
        except Exception as e:
            return str(e)

    result = get_player_data()
    
    if isinstance(result, pd.DataFrame):
        st.dataframe(result, use_container_width=True)
    else:
        st.warning(f"데이터 상태: {result}")
        st.info("데이터가 보이지 않는다면, RapidAPI 대시보드에서 해당 API를 구독했는지 다시 한번 확인해주세요.")
