import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# API 설정
API_KEY = "9c3c5d2369ad9163a19c3e88dfa1f9c5"

# --- 1. 배당 데이터 호출 ---
def get_mlb_odds_styled():
    try:
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {"apiKey": API_KEY, "regions": "us", "markets": "h2h"}
        response = requests.get(url, params=params)
        data = response.json()
        results = []
        for game in data:
            if not game.get('bookmakers'): continue
            dt = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
            odds = game['bookmakers'][0]['markets'][0]['outcomes']
            home_price = next((o['price'] for o in odds if o['name'] == game['home_team']), 0.0)
            away_price = next((o['price'] for o in odds if o['name'] == game['away_team']), 0.0)
            results.append({"일시": dt.strftime('%m/%d %H:%M'), "원정": game['away_team'], "홈": game['home_team'], "원정(승)": float(away_price), "홈(승)": float(home_price)})
        return pd.DataFrame(results)
    except: return pd.DataFrame()

# --- 2. 화면 구성 ---
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 분석 시스템")

# [상단 설정창 복구]
col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

# [좌우 분할 구성]
main_left, main_right = st.columns([1.5, 2.5])

with main_left:
    # [탭 및 분석 모드 복구]
    tab1, tab2 = st.tabs(["⚡ 자동 분석", "🔍 수동 정밀 분석"])
    with tab1:
        c1, c2 = st.columns(2)
        a_code = c1.text_input("원정 팀")
        h_code = c2.text_input("홈 팀")
        if st.button("분석 실행 (자동)"):
            st.success(f"{a_code} vs {h_code} 전력 분석 중...")
    with tab2:
        h_man = st.text_area("홈 팀 선수 명단")
        a_man = st.text_area("원정 팀 선수 명단")
        if st.button("분석 실행 (수동)"):
            st.write("선수단 정밀 분석 시작...")

with main_right:
    st.subheader("📋 실시간 배당률 (Proto Style)")
    @st.fragment(run_every="60s")
    def render_odds_table():
        df = get_mlb_odds_styled()
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("데이터를 불러오는 중입니다...")
    render_odds_table()
