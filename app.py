import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time

# --- [DB 및 매칭 로직] ---
# 실제 운영 시에는 이 딕셔너리를 외부 JSON/CSV 파일로 분리하여 관리하세요
team_db = {"bos": ["R.Devers", "J.Duran", "T.Casas", "M.Yoshida", "C.Rafaela", "D.Hamilton", "R.McGuire", "V.Abreu", "B.Wong"],
           "nyy": ["A.Judge", "J.Soto", "G.Torres", "A.Verdugo", "A.Volpe", "O.Cabrera", "J.Trevino", "D.LeMahieu", "A.Wells"]}

player_to_team = {"r.devers": "bos", "a.judge": "nyy", "j.soto": "nyy"} # 선수-팀 매핑

def resolve_lineup(user_input):
    """입력값을 분석하여 최종 라인업 리스트를 반환하는 로직"""
    user_input = user_input.lower().strip()
    # 1. 팀코드로 바로 검색
    if user_input in team_db:
        return team_db[user_input]
    # 2. 선수이름으로 검색
    if user_input in player_to_team:
        return team_db[player_to_team[user_input]]
    # 3. 쉼표 구분 입력일 경우 그대로 리스트화
    return [p.strip() for p in user_input.split(',')]

# --- [기존 기능 유지] ---
@st.cache_data(ttl=3600)
def get_live_lineup(team_code):
    # 크롤링 로직 (기존과 동일)
    return ["Player1", "Player2", "Player3"]

def run_stat_based_simulation(h_lineup, a_lineup, days_range):
    # 라인업 리스트를 받아 시뮬레이션 수행
    base_prob = 0.5
    volatility = 0.05 * (30 / days_range)
    return max(0.2, min(0.8, base_prob + np.random.normal(0, volatility)))

# --- [UI 영역] ---
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜 선택", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 코드 (예: BOS)", key="h_auto")
    a_code = st.text_input("원정 팀 코드 (예: NYY)", key="a_auto")
    if st.button("분석 실행 (기간 적용)"):
        h_lineup = get_live_lineup(h_code)
        a_lineup = get_live_lineup(a_code)
        prob = run_stat_based_simulation(h_lineup, a_lineup, days_range)
        st.metric("홈 팀 승리 확률", f"{prob*100:.1f}%")

with tab2:
    st.info("팀명, 선수명, 또는 라인업을 자유롭게 입력하세요.")
    h_man = st.text_area("홈 팀/선수 입력", key="h_man")
    a_man = st.text_area("원정 팀/선수 입력", key="a_man")
    if st.button("분석 실행"):
        # 매칭 로직 적용
        h_lineup = resolve_lineup(h_man)
        a_lineup = resolve_lineup(a_man)
        prob = run_stat_based_simulation(h_lineup, a_lineup, days_range)
        st.metric("홈 팀 승리 확률", f"{prob*100:.1f}%")
