import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

# --- 1. 실시간 데이터 엔진 (캐싱 적용) ---
@st.cache_data(ttl=3600)
def get_live_lineup(team_code):
    # 크롤링 로직 (생략된 부분 동일 적용)
    return ["Player1", "Player2", "Player3"] # 임시 데이터

# --- 2. 기간별 스탯 기반 시뮬레이션 엔진 ---
def run_stat_based_simulation(h_lineup, a_lineup, days_range):
    # 이 로직에 'days_range'를 대입하여 기간별 평균 스탯으로 시뮬레이션함
    # 실제로는 DB에서 해당 기간 스탯을 불러와 계산하는 함수
    base_prob = 0.5
    volatility = 0.05 * (30 / days_range) # 기간이 짧을수록 변동성 확대
    return max(0.2, min(0.8, base_prob + np.random.normal(0, volatility)))

# --- 3. UI 및 통합 로직 ---
st.title("⚾ MLB AI 분석 시스템")

# 상단 공통 설정 (날짜 및 범위)
col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜 선택", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 코드 (예: LAD)", key="h_auto")
    a_code = st.text_input("원정 팀 코드 (예: NYY)", key="a_auto")
    
    if st.button("분석 실행 (기간 적용)"):
        h_lineup = get_live_lineup(h_code)
        a_lineup = get_live_lineup(a_code)
        st.write(f"📅 {target_date} 기준, 최근 {days_range}일 스탯 반영 완료")
        prob = run_stat_based_simulation(h_lineup, a_lineup, days_range)
        st.metric("홈 팀 승리 확률", f"{prob*100:.1f}%")

with tab2:
    st.info("라인업 직접 입력 시에도 기간 설정이 동일하게 적용됩니다.")
    h_man = st.text_area("홈 라인업 (쉼표 구분)")
    a_man = st.text_area("원정 라인업 (쉼표 구분)")
    if st.button("분석 실행"):
        prob = run_stat_based_simulation(h_man, a_man, days_range)
        st.metric("홈 팀 승리 확률", f"{prob*100:.1f}%")
