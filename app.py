import streamlit as st
import requests
import time
from datetime import datetime

# 직접 심어드린 API 키
API_KEY = "9c3c5d2369ad9163a19c3e88dfa1f9c5"

# --- 1. 실시간 배당 데이터 가져오기 ---
def get_realtime_odds(fixture_id):
    try:
        # 실제 API 서비스의 엔드포인트와 파라미터 구조에 맞춰 사용하세요
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {"apiKey": API_KEY, "regions": "us", "markets": "h2h"}
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# --- 2. 실시간 배당 UI (5초마다 업데이트) ---
@st.fragment(run_every="5s")
def display_live_odds():
    st.write("### ⚡ 실시간 MLB 배당 정보")
    data = get_realtime_odds("mlb_fixture")
    
    if isinstance(data, list) and len(data) > 0:
        # 첫 번째 경기 데이터 예시 추출
        game = data[0]
        home_team = game['home_team']
        away_team = game['away_team']
        
        col1, col2 = st.columns(2)
        col1.metric(f"{home_team} 승", "1.95") # 실제 API 데이터로 파싱 필요
        col2.metric(f"{away_team} 승", "1.85")
    else:
        st.info("데이터를 불러오는 중입니다...")

# --- 3. UI 고정 (이전 구조 유지) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    # 실시간 배당 영역 추가
    display_live_odds()
    
    h_code = st.text_input("홈 팀 코드", key="h_auto")
    if st.button("분석 실행 (자동)"):
        st.write("분석 엔진이 가동되었습니다.")

with tab2:
    st.info("수동 분석 모드입니다.")
