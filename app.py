import streamlit as st
import requests
import pandas as pd
from datetime import datetime

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
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            return pd.DataFrame(response.json().get('data', []))
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# --- 2. 화면 구성 ---
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 분석 시스템")

# [상단 설정창 복구]
col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

st.divider() # 상단과 하단 구분선

# [하단 좌우 분할]
main_left, main_right = st.columns([1.5, 2.5])

with main_left:
    st.subheader("📊 분석 엔진")
    tab1, tab2 = st.tabs(["⚡ 자동 분석", "🔍 수동 분석"])
    with tab1:
        a_code = st.text_input("원정 팀")
        h_code = st.text_input("홈 팀")
        if st.button("자동 분석 시작"):
            st.success(f"{target_date} 기준 {a_code} vs {h_code} 분석 중...")
    with tab2:
        st.text_area("홈 팀 선수 명단")
        st.text_area("원정 팀 선수 명단")
        if st.button("정밀 분석 시작"):
            st.info("입력된 명단 기반 분석 수행")

with main_right:
    st.subheader("⚡ 실시간 배당 대시보드")
    @st.fragment(run_every="60s")
    def display_odds():
        df = get_live_odds()
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("데이터 수신 대기 중... (ID 확인 필요)")
    display_odds()
