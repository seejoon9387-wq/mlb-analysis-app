import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# API 설정 (직접 삽입)
API_KEY = "9c3c5d2369ad9163a19c3e88dfa1f9c5"

# --- 1. 배당 데이터 최적화 호출 ---
def get_mlb_odds_df():
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
            home_odds = next((o['price'] for o in odds if o['name'] == game['home_team']), 0.0)
            
            results.append({
                "일시": dt.strftime('%m/%d %H:%M'),
                "매치업": f"{game['away_team']} vs {game['home_team']}",
                "홈승배당": float(home_odds)
            })
        return pd.DataFrame(results)
    except:
        return pd.DataFrame()

# --- 2. 최적화된 레이아웃 ---
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 분석 시스템")

left_col, right_col = st.columns([1, 2])

with right_col:
    st.subheader("⚡ 실시간 배당 대시보드")
    
    @st.fragment(run_every="60s")
    def render_odds():
        df = get_mlb_odds_df()
        if not df.empty:
            # 데이터프레임 스타일 최적화
            st.dataframe(
                df, 
                use_container_width=True, 
                hide_index=True,
                column_config={"홈승배당": st.column_config.NumberColumn(format="%.2f")}
            )
        else:
            st.warning("데이터를 불러오는 중입니다...")
    render_odds()

with left_col:
    st.subheader("📊 분석 및 예측")
    tab1, tab2 = st.tabs(["⚡ 자동 분석", "🔍 정밀 분석"])
    
    with tab1:
        away = st.text_input("원정 팀")
        home = st.text_input("홈 팀")
        if st.button("분석 실행"):
            st.info(f"{away} vs {home} 예측 엔진 가동...")
            
    with tab2:
        st.text_area("선수 명단 입력")
        if st.button("분석 시작"):
            st.info("데이터 분석 엔진 구동 중...")
