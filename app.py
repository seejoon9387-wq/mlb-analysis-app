import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# RapidAPI 설정
API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
HOST = "odds-feed.p.rapidapi.com"

# --- 1. 자동화된 실시간 데이터 호출 ---
def get_live_odds():
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
    
    try:
        # 단계 1: 현재 진행 중인 MLB 경기 ID 목록을 자동으로 가져옴
        # (API 문서상 'events' 관련 엔드포인트 확인 필요)
        event_url = "https://odds-feed.p.rapidapi.com/api/v1/events/live"
        event_res = requests.get(event_url, headers=headers, timeout=5)
        
        if event_res.status_code == 200:
            events = event_res.json().get('data', [])
            if not events:
                return None, "현재 진행 중인 경기가 없습니다."
            
            # 상위 5개 경기 ID만 추출
            ids = ",".join([str(e['id']) for e in events[:5]])
            
            # 단계 2: 해당 ID들로 실시간 배당 조회
            odds_url = "https://odds-feed.p.rapidapi.com/api/v1/markets/feed"
            params = {"placing": "LIVE", "event_ids": ids, "market_name": "1X2"}
            odds_res = requests.get(odds_url, headers=headers, params=params)
            
            return pd.DataFrame(odds_res.json().get('data', [])), None
        return None, "경기 목록을 불러올 수 없습니다."
    except Exception as e:
        return None, str(e)

# --- 2. 화면 구성 (안전하게 유지) ---
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 분석 시스템")

# [상단 설정창]
col1, col2 = st.columns(2)
col1.date_input("분석 날짜", datetime.now())
col2.slider("분석 범위", 1, 30, 7)
st.divider()

# [하단 좌우 분할]
left, right = st.columns([1.5, 2.5])

with left:
    st.subheader("📊 분석 엔진")
    st.text_input("원정 팀")
    st.text_input("홈 팀")
    st.button("자동 분석 시작")

with right:
    st.subheader("⚡ 실시간 배당 대시보드")
    df, error = get_live_odds()
    
    if df is not None:
        st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"데이터 수신 불가: {error}")
