import streamlit as st
import requests
import pandas as pd

# RapidAPI 설정
API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
HOST = "odds-feed.p.rapidapi.com"

def get_live_odds():
    url = "https://odds-feed.p.rapidapi.com/api/v1/markets/feed"
    querystring = {
        "placing": "LIVE",
        "market_name": "1X2",
        "bet_type": "BACK",
        "page": "0",
        "event_ids": "845,123,435,22,842,844,845",
        "period": "FULL_TIME_AND_OT"
    }
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": HOST,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = response.json()
            # 데이터 구조에 맞게 파싱 (API 응답 형식에 따라 수정 필요)
            # 여기서는 예시로 'data' 내의 리스트를 가정합니다.
            return pd.DataFrame(data.get('data', []))
        else:
            st.error(f"API 호출 실패: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터 로딩 오류: {e}")
        return pd.DataFrame()

# --- UI 레이아웃 ---
st.set_page_config(page_title="MLB Live Odds", layout="wide")
st.title("⚾ 실시간 배당 피드 (RapidAPI)")

if st.button("실시간 배당 업데이트"):
    df = get_live_odds()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("현재 수신된 배당 데이터가 없습니다.")
