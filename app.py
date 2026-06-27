import streamlit as st
import requests
import pandas as pd

# RapidAPI 설정
API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
HOST = "odds-feed.p.rapidapi.com"

# --- 1. 배당 데이터 가져오기 ---
def get_live_odds():
    url = "https://odds-feed.p.rapidapi.com/api/v1/markets/feed"
    querystring = {
        "placing": "LIVE",
        "market_name": "1X2",
        "bet_type": "BACK",
        "page": "0",
        "event_ids": "845,123,435,22,842,844,845",
        "period": "FULL_TIME_AND_OT"
    }
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": HOST
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data.get('data', []))
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# --- 2. 화면 구성 (레이아웃 고정) ---
st.set_page_config(page_title="MLB AI Analyst", layout="wide")

st.title("⚾ MLB AI 분석 시스템")

# 상단 탭으로 분석 방식 구분
tab_auto, tab_manual = st.tabs(["⚡ 자동 분석", "🔍 수동 분석"])

# 좌우 레이아웃을 위한 컨테이너 생성
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("📊 분석 설정")
    with tab_auto:
        a_code = st.text_input("원정 팀")
        h_code = st.text_input("홈 팀")
        if st.button("자동 분석 시작"):
            st.info("실시간 데이터 분석 중...")
            
    with tab_manual:
        st.text_area("홈 팀 선수 명단")
        st.text_area("원정 팀 선수 명단")
        if st.button("수동 분석 시작"):
            st.info("정밀 분석 수행 중...")

with col_right:
    st.subheader("⚡ 실시간 배당 대시보드")
    # 배당판을 60초마다 갱신
    @st.fragment(run_every="60s")
    def display_odds():
        df = get_live_odds()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("현재 실시간 배당 데이터가 없습니다.")
    display_odds()
