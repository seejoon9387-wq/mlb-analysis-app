import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Streamlit 설정
st.set_page_config(page_title="MLB AI Analyst", layout="wide")

# API 설정
API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
HOST = "odds-feed.p.rapidapi.com"

# --- 1. 안전한 데이터 호출 함수 ---
def get_live_odds():
    try:
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
        
        response = requests.get(url, headers=headers, params=querystring, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data.get('data', []))
        else:
            return pd.DataFrame() # 에러 발생 시 빈 DF 반환
    except Exception:
        return pd.DataFrame() # 예외 발생 시 빈 DF 반환

# --- 2. 화면 구성 ---
st.title("⚾ MLB AI 분석 시스템")

# [상단 설정창] - UI가 항상 유지되도록 최상단 배치
col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)
st.divider()

# [좌우 분할]
main_left, main_right = st.columns([1.5, 2.5])

with main_left:
    st.subheader("📊 분석 엔진")
    tab1, tab2 = st.tabs(["⚡ 자동 분석", "🔍 수동 분석"])
    with tab1:
        a_code = st.text_input("원정 팀")
        h_code = st.text_input("홈 팀")
        st.button("자동 분석 시작")
    with tab2:
        st.text_area("홈 팀 선수 명단")
        st.text_area("원정 팀 선수 명단")
        st.button("정밀 분석 시작")

with main_right:
    st.subheader("⚡ 실시간 배당 대시보드")
    
    # 데이터를 가져오는 부분만 별도 함수로 격리
    df = get_live_odds()
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        # 데이터가 없어도 UI는 사라지지 않음
        st.info("현재 실시간 배당 데이터가 수신되지 않고 있습니다. (이벤트 ID를 확인하세요)")
