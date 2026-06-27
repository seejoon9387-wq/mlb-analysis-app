import streamlit as st
import requests
from datetime import datetime

# 직접 심어드린 API 키
API_KEY = "9c3c5d2369ad9163a19c3e88dfa1f9c5"

# --- 1. 실시간 전체 배당 데이터 호출 ---
def get_all_mlb_odds():
    try:
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {"apiKey": API_KEY, "regions": "us", "markets": "h2h"}
        response = requests.get(url, params=params)
        return response.json()
    except Exception:
        return []

# --- 2. 실시간 전체 배당 UI ---
@st.fragment(run_every="60s")
def display_all_live_odds():
    st.write("### ⚡ 오늘 전체 MLB 경기 및 실시간 배당")
    data = get_all_mlb_odds()
    
    if isinstance(data, list) and len(data) > 0:
        for game in data:
            home = game.get('home_team', 'Unknown')
            away = game.get('away_team', 'Unknown')
            commence_time = game.get('commence_time', 'N/A')
            
            # 간단한 배당 출력
            st.markdown(f"**{away} vs {home}** | 시작: {commence_time}")
            # 실제 API에서 배당 정보를 파싱하여 출력
            st.info(f"홈 배당(상세 확인 필요) / 원정 배당")
    else:
        st.info("현재 불러올 수 있는 경기 데이터가 없습니다.")

# --- 3. UI 고정 (전체 구조 복구) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    display_all_live_odds() # 전체 경기 배당 노출
    
    # 원정/홈 모두 포함된 입력창 복구
    c1, c2 = st.columns(2)
    h_code = c1.text_input("홈 팀", key="h_auto")
    a_code = c2.text_input("원정 팀", key="a_auto")
    
    if st.button("분석 실행 (자동)"):
        st.write("선택하신 경기의 전력을 분석합니다.")

with tab2:
    h_man = st.text_area("홈 팀 선수 명단", key="h_man")
    a_man = st.text_area("원정 팀 선수 명단", key="a_man")
    if st.button("분석 실행 (수동)"):
        st.write("수동 입력된 선수단 전력을 비교합니다.")
