import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. UI 및 페이지 설정 (항상 고정)
st.set_page_config(page_title="MLB AI Analyst", layout="wide")

# 사이드바나 헤더를 활용해 레이아웃 붕괴 방지
st.title("⚾ MLB AI 분석 시스템")

# [항상 고정되는 상단 컨트롤러]
with st.container():
    c1, c2 = st.columns(2)
    target_date = c1.date_input("분석 날짜", datetime.now())
    days_range = c2.slider("분석 범위 (최근 N일)", 1, 30, 7)
    st.divider()

# [좌우 레이아웃 고정]
col_left, col_right = st.columns([1, 2])

# 2. 왼쪽: 분석창 (고정)
with col_left:
    st.subheader("📊 분석 엔진")
    tab1, tab2 = st.tabs(["⚡ 자동 분석", "🔍 수동 분석"])
    with tab1:
        st.text_input("원정 팀")
        st.text_input("홈 팀")
        st.button("자동 분석 시작")
    with tab2:
        st.text_area("홈 팀 선수 명단")
        st.text_area("원정 팀 선수 명단")
        st.button("정밀 분석 시작")

# 3. 오른쪽: 배당판 (데이터 없어도 UI 유지)
with col_right:
    st.subheader("⚡ 실시간 배당 대시보드")
    
    # API-Baseball 설정 (구독 후 사용)
    RAPID_API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    
    def fetch_odds():
        url = "https://api-baseball.p.rapidapi.com/odds"
        headers = {
            "x-rapidapi-key": RAPID_API_KEY,
            "x-rapidapi-host": "api-baseball.p.rapidapi.com"
        }
        querystring = {"league": "1", "season": "2026"}
        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return pd.DataFrame(data.get('response', []))
            return pd.DataFrame()
        except:
            return pd.DataFrame()

    df = fetch_odds()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("데이터를 가져올 수 없습니다. API-Baseball을 구독했는지 확인하세요.")
