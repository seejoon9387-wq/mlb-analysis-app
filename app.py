import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# API 설정
API_KEY = "9c3c5d2369ad9163a19c3e88dfa1f9c5"

# --- 1. 데이터 호출 및 사이트 유사 구조로 파싱 ---
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
            
            # 홈/원정 데이터 추출
            home_team = game['home_team']
            away_team = game['away_team']
            home_price = next((o['price'] for o in odds if o['name'] == home_team), 0.0)
            away_price = next((o['price'] for o in odds if o['name'] == away_team), 0.0)
            
            results.append({
                "일시": dt.strftime('%m/%d %H:%M'),
                "원정팀": away_team,
                "홈팀": home_team,
                "원정(승)": float(away_price),
                "홈(승)": float(home_price)
            })
        return pd.DataFrame(results)
    except:
        return pd.DataFrame()

# --- 2. 화면 구성 (Wide Layout) ---
st.set_page_config(page_title="MLB 배당판", layout="wide")
st.title("⚾ MLB 배당 정보 보드")

# 좌우 배치: 분석창(왼쪽) / 배당판(오른쪽)
col_left, col_right = st.columns([1, 3])

with col_right:
    st.subheader("📋 실시간 배당률 (Proto Style)")
    
    @st.fragment(run_every="60s")
    def render_odds_table():
        df = get_mlb_odds_styled()
        if not df.empty:
            # 사이트와 유사한 그리드 형태의 테이블 출력
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "원정(승)": st.column_config.NumberColumn(format="%.2f"),
                    "홈(승)": st.column_config.NumberColumn(format="%.2f")
                }
            )
        else:
            st.warning("데이터를 불러오는 중입니다...")
    render_odds_table()

with col_left:
    st.subheader("📊 분석 엔진")
    with st.container():
        a_code = st.text_input("원정 팀 입력")
        h_code = st.text_input("홈 팀 입력")
        if st.button("분석 실행"):
            st.info(f"{a_code} vs {h_code} 데이터 분석 중...")
