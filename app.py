import streamlit as st
import requests
from datetime import datetime

# API 키
API_KEY = "9c3c5d2369ad9163a19c3e88dfa1f9c5"

# --- 1. 실시간 배당 데이터 호출 ---
def get_all_mlb_odds():
    try:
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {"apiKey": API_KEY, "regions": "us", "markets": "h2h"}
        response = requests.get(url, params=params)
        return response.json()
    except Exception:
        return []

# --- 2. 화면 구성 ---
st.set_page_config(page_title="MLB AI Analyst", layout="wide") # wide 모드로 변경
st.title("⚾ MLB AI 분석 시스템")

# 좌우 분할 (왼쪽: 분석 / 오른쪽: 실시간 배당)
left_col, right_col = st.columns([2, 1])

with right_col:
    st.write("### ⚡ 실시간 MLB 배당")
    # 배당 데이터 업데이트 프래그먼트
    @st.fragment(run_every="60s")
    def display_odds():
        data = get_all_mlb_odds()
        if isinstance(data, list):
            for game in data[:10]: # 상위 10개 경기만 표시
                st.write(f"**{game.get('away_team')} vs {game.get('home_team')}**")
                st.caption(f"시작: {game.get('commence_time')}")
                st.divider()
        else:
            st.info("데이터 로딩 중...")
    display_odds()

with left_col:
    tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])
    
    with tab1:
        # 원정/홈 입력창 복구
        col_a, col_b = st.columns(2)
        a_code = col_a.text_input("원정 팀 (Away)")
        h_code = col_b.text_input("홈 팀 (Home)")
        
        if st.button("분석 실행 (자동)"):
            st.success(f"{a_code} vs {h_code} 분석을 시작합니다.")
            
    with tab2:
        h_man = st.text_area("홈 팀 선수 명단")
        a_man = st.text_area("원정 팀 선수 명단")
        if st.button("분석 실행 (수동)"):
            st.write("입력된 선수단 전력을 분석합니다.")
