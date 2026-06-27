import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# API 키
API_KEY = "9c3c5d2369ad9163a19c3e88dfa1f9c5"

# --- 1. 실시간 배당 호출 및 변동 비교 로직 ---
def get_mlb_odds_with_trend():
    try:
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {"apiKey": API_KEY, "regions": "us", "markets": "h2h"}
        response = requests.get(url, params=params)
        data = response.json()
        
        results = []
        for game in data:
            # 날짜 및 시간 파싱
            dt = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
            
            # 배당 파싱 (첫 번째 북메이커 기준 예시)
            odds = game['bookmakers'][0]['markets'][0]['outcomes']
            home_odds = next(o['price'] for o in odds if o['name'] == game['home_team'])
            
            results.append({
                "날짜": dt.strftime('%m/%d %H:%M'),
                "원정": game['away_team'],
                "홈": game['home_team'],
                "홈승배당": home_odds
            })
        return pd.DataFrame(results)
    except:
        return pd.DataFrame()

# --- 2. 화면 구성 (좌우 분할) ---
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 분석 시스템")

# 상태 저장: 배당 변동 추적용
if 'prev_df' not in st.session_state:
    st.session_state.prev_df = pd.DataFrame()

left_col, right_col = st.columns([1.5, 2.5])

with right_col:
    st.subheader("⚡ 실시간 배당 변동 모니터링")
    
    @st.fragment(run_every="60s")
    def display_odds_with_trend():
        df = get_mlb_odds_with_trend()
        
        if not df.empty:
            # 이전 데이터와 비교하여 화살표 표시
            if not st.session_state.prev_df.empty:
                # 간단한 비교 로직 (병합 후 배당 차이 계산)
                df = df.merge(st.session_state.prev_df[['홈', '홈승배당']], on='홈', suffixes=('', '_prev'))
                df['변동'] = df.apply(lambda x: '▲' if x['홈승배당'] > x['홈승배당_prev'] else ('▼' if x['홈승배당'] < x['홈승배당_prev'] else '-'), axis=1)
            
            st.table(df[['날짜', '원정', '홈', '홈승배당', '변동']])
            st.session_state.prev_df = df
        else:
            st.info("데이터를 불러오는 중입니다...")
            
    display_odds_with_trend()

with left_col:
    # 분석창 (기존과 동일)
    tab1, tab2 = st.tabs(["⚡ 자동 분석", "🔍 수동 분석"])
    with tab1:
        c1, c2 = st.columns(2)
        a_code = c1.text_input("원정 팀")
        h_code = c2.text_input("홈 팀")
        if st.button("분석 실행"):
            st.success(f"{a_code} vs {h_code} 전력 분석 완료")
