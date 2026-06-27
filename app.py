import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 페이지 설정 (전체 레이아웃 고정)
st.set_page_config(page_title="MLB AI Analyst", layout="wide")

# 상단 UI (항상 고정)
st.title("⚾ MLB AI 분석 시스템")
c_top1, c_top2 = st.columns(2)
target_date = c_top1.date_input("분석 날짜", datetime.now())
days_range = c_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)
st.divider()

# 좌우 레이아웃 (항상 고정)
left_col, right_col = st.columns([1.5, 2.5])

# --- 왼쪽: 분석 도구 (항상 고정) ---
with left_col:
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

# --- 오른쪽: 배당판 (데이터가 없어도 UI 유지) ---
with right_col:
    st.subheader("⚡ 실시간 배당 대시보드")
    
    # API 키 및 설정
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    
    # [중요] RapidAPI 엔드포인트 확인 필요
    # 현재 URL은 예시입니다. RapidAPI 대시보드에서 보신 정확한 URL로 수정하세요.
    url = "https://odds-feed.p.rapidapi.com/api/v1/markets/feed"
    
    try:
        # 데이터 호출 시도
        # (테스트용으로 event_ids를 제거하거나 실제 ID로 채워주세요)
        response = requests.get(url, headers={"x-rapidapi-key": API_KEY, "x-rapidapi-host": "odds-feed.p.rapidapi.com"}, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            st.dataframe(pd.DataFrame(data.get('data', [])), use_container_width=True)
        else:
            st.error(f"API 호출 실패 (코드: {response.status_code})")
            st.write("RapidAPI 대시보드에서 엔드포인트가 맞는지 확인해 주세요.")
            
    except Exception as e:
        st.warning("데이터 수신 대기 중... 설정 확인이 필요합니다.")
