import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# API 키
API_KEY = "9c3c5d2369ad9163a19c3e88dfa1f9c5"

# --- 1. 데이터 호출 및 데이터프레임 변환 ---
def get_all_mlb_odds():
    try:
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {"apiKey": API_KEY, "regions": "us", "markets": "h2h"}
        response = requests.get(url, params=params)
        data = response.json()
        
        # 가독성을 위해 리스트를 데이터프레임으로 변환
        processed_data = []
        for game in data:
            processed_data.append({
                "원정": game.get('away_team'),
                "홈": game.get('home_team'),
                "시간": game.get('commence_time')[11:16], # 시간만 추출
            })
        return pd.DataFrame(processed_data)
    except:
        return pd.DataFrame()

# --- 2. 화면 구성 (Wide Layout) ---
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 분석 시스템")

left_col, right_col = st.columns([1.5, 2.5]) # 우측 배당창 가독성을 위해 비율 조정

with right_col:
    st.subheader("⚡ 실시간 MLB 배당 대시보드")
    
    @st.fragment(run_every="60s")
    def display_odds_table():
        df = get_all_mlb_odds()
        if not df.empty:
            # 테이블 가독성 향상
            st.table(df.style.set_properties(**{'text-align': 'center'}))
        else:
            st.info("데이터 로딩 중...")
    display_odds_table()

with left_col:
    tab1, tab2 = st.tabs(["⚡ 자동 분석", "🔍 수동 분석"])
    with tab1:
        c1, c2 = st.columns(2)
        a_code = c1.text_input("원정(Away)")
        h_code = c2.text_input("홈(Home)")
        if st.button("자동 분석 시작"):
            st.success(f"{a_code} vs {h_code} 전력 산출 중...")
            
    with tab2:
        h_man = st.text_area("홈 팀 명단")
        a_man = st.text_area("원정 팀 명단")
        if st.button("정밀 분석"):
            st.write("선수별 스탯 정밀 분석 엔진 가동")
