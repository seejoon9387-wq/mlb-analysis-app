import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# RapidAPI 설정
API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
HOST = "odds-feed.p.rapidapi.com"

# --- 1. 실시간 경기 목록 및 배당 호출 ---
def get_live_odds():
    # 1단계: 진행 중인 경기 ID 목록을 가져오는 엔드포인트 호출 (가정)
    # 실제 API 문서에서 'List Events' 엔드포인트를 확인해야 합니다.
    list_url = "https://odds-feed.p.rapidapi.com/api/v1/events/live" # 예시 엔드포인트
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
    
    try:
        # 경기 목록 조회
        list_res = requests.get(list_url, headers=headers)
        if list_res.status_code == 200:
            events = list_res.json().get('data', [])
            if not events: return pd.DataFrame()
            
            # 경기 ID만 추출
            event_ids = ",".join([str(e['id']) for e in events[:5]]) 
            
            # 2단계: 가져온 ID로 배당 호출
            odds_url = "https://odds-feed.p.rapidapi.com/api/v1/markets/feed"
            params = {"placing": "LIVE", "event_ids": event_ids, "market_name": "1X2"}
            odds_res = requests.get(odds_url, headers=headers, params=params)
            
            return pd.DataFrame(odds_res.json().get('data', []))
        return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터 통신 오류: {e}")
        return pd.DataFrame()

# ... (이하 UI 구성 코드는 동일)
