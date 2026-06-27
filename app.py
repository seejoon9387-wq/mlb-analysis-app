import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# API 키
API_KEY = "9c3c5d2369ad9163a19c3e88dfa1f9c5"

# --- 1. 배당 데이터 호출 함수 ---
def get_mlb_odds_with_trend():
    try:
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {"apiKey": API_KEY, "regions": "us", "markets": "h2h"}
        response = requests.get(url, params=params)
        data = response.json()
        
        results = []
        for game in data:
            dt = datetime.fromisoformat(game['commence_time'].replace('Z', '+00:00'))
            # bookmakers가 비어있을 수 있으므로 예외 처리 추가
            if not game.get('bookmakers'): continue
            
            odds = game['bookmakers'][0]['markets'][0]['outcomes']
            home_odds = next((o['price'] for o in odds if o['name'] == game['home_team']), 0.0)
            
            results.append({
                "날짜": dt.strftime('%m/%d %H:%M'),
                "원정": game['away_team'],
                "홈": game['home_team'],
                "홈승배당": float(home_odds)
            })
        return pd.DataFrame(results)
    except:
        return pd.DataFrame()

# --- 2. 실시간 변동 테이블 생성부 (에러 방어 로직 포함) ---
@st.fragment(run_every="60s")
def display_odds_with_trend():
    df = get_mlb_odds_with_trend()
    
    if not df.empty:
        # 데이터프레임 초기화 확인
        if 'prev_df' not in st.session_state or st.session_state.prev_df.empty:
            df['변동'] = '-' # 첫 로딩 시 기본값
        else:
            # 이전 데이터와 병합
            df = df.merge(st.session_state.prev_df[['홈', '홈승배당']], on='홈', how='left', suffixes=('', '_prev'))
            # 비교 로직: 이전 데이터가 없으면 '-' 있으면 화살표
            df['변동'] = df.apply(lambda x: '▲' if pd.notnull(x['홈승배당_prev']) and x['홈승배당'] > x['홈승배당_prev'] 
                                   else ('▼' if pd.notnull(x['홈승배당_prev']) and x['홈승배당'] < x['홈승배당_prev'] else '-'), axis=1)
            # 불필요 컬럼 제거
            df = df.drop(columns=['홈승배당_prev'], errors='ignore')
            
        st.table(df[['날짜', '원정', '홈', '홈승배당', '변동']])
        # 현재 df를 다음 번 비교를 위해 저장
        st.session_state.prev_df = df
    else:
        st.info("데이터를 불러오는 중입니다...")

# --- 3. UI ---
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 분석 시스템")

# 좌우 레이아웃 구성
left_col, right_col = st.columns([1.5, 2.5])

with right_col:
    st.subheader("⚡ 실시간 배당 변동 모니터링")
    display_odds_with_trend()

with left_col:
    st.write("분석 입력창 (좌측)")
