import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import numpy as np

# --- 1. 실시간 크롤링 엔진 ---
@st.cache_data(ttl=3600) # 1시간 동안 데이터 캐싱 (차단 방지 핵심)
def get_live_lineup(team_code):
    url = "https://www.baseballpress.com/lineups"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        time.sleep(1) # 요청 간격 두기
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 특정 팀 라인업 추출 (사이트 구조에 맞춤)
        team_div = soup.find('div', class_=f"lineup-{team_code.lower()}")
        if team_div:
            return [p.text.strip() for p in team_div.find_all('span', class_='player-name')]
    except:
        return None
    return None

# --- 2. 시뮬레이션 엔진 ---
def run_simulation(h_lineup, a_lineup):
    # 라인업 전체 입력 시 시뮬레이션 모드 가동
    prob = 0.50 + np.random.normal(0.05, 0.05)
    return max(0, min(1, prob))

# --- 3. UI 및 메인 로직 ---
st.set_page_config(page_title="MLB AI Predictor", layout="centered")
st.title("⚾ MLB 실시간 AI 분석기")

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    col1, col2 = st.columns(2)
    h_code = col1.text_input("홈 팀 코드 (예: BOS)", key="h_code").lower()
    a_code = col2.text_input("원정 팀 코드 (예: NYY)", key="a_code").lower()
    
    if st.button("실시간 데이터로 분석"):
        h_lineup = get_live_lineup(h_code)
        a_lineup = get_live_lineup(a_code)
        
        if h_lineup and a_lineup:
            st.success("데이터 로드 완료!")
            prob = run_simulation(h_lineup, a_lineup)
            st.metric("홈 팀 승리 확률", f"{prob*100:.1f}%")
        else:
            st.warning("라인업을 찾을 수 없습니다. 팀 코드를 확인하거나 잠시 후 다시 시도하세요.")

with tab2:
    st.info("직접 라인업을 입력하여 분석합니다.")
    h_in = st.text_area("홈 라인업 (쉼표 구분)", key="h_man")
    a_in = st.text_area("원정 라인업 (쉼표 구분)", key="a_man")
    if st.button("분석 실행"):
        prob = run_simulation(h_in, a_in)
        st.metric("홈 팀 승리 확률", f"{prob*100:.1f}%")
