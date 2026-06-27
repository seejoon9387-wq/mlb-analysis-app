import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime

# --- 1. 유틸리티 ---
def get_team_id_by_name(input_name):
    team_db = {
        '볼티': 'BAL', '양키스': 'NYY', '보스턴': 'BOS', '다저스': 'LAD', '메츠': 'NYM',
        '필리스': 'PHI', '컵스': 'CHC', '화이트삭스': 'CWS', '클리블랜드': 'CLE', '휴스턴': 'HOU'
    }
    return team_db.get(input_name, input_name)

@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path): return None
    df = pd.read_csv(file_path)
    df['game_date'] = pd.to_datetime(df['game_date'])
    df['is_strikeout'] = df['events'].apply(lambda x: 1 if x == 'strikeout' else 0)
    for col in ['release_speed', 'launch_speed', 'is_whiff', 'is_strikeout']:
        if col in df.columns: df[col] = df[col].fillna(0)
    return df

# --- 2. 분석 엔진 ---
def run_full_analysis(mode, h_val, a_val, selected_date, days):
    # 환경 변수 가중치 (내부 연산)
    home_field_advantage = 1.04
    night_game_bonus = 1.02
    
    score_h = h_val * home_field_advantage
    score_a = a_val * night_game_bonus
    
    # 시뮬레이션
    iterations = 100000
    sim_h = np.random.normal(score_h, 3, iterations)
    sim_a = np.random.normal(score_a, 3, iterations)
    return np.mean(sim_h > sim_a), sim_h, sim_a

# --- 3. 프론트엔드 UI ---
st.title("⚾ MLB 최종 통합 분석기")

# [기능 1: 환경 설정]
with st.sidebar:
    st.header("설정 및 환경")
    selected_date = st.date_input("경기 날짜", datetime.date(2026, 6, 27))
    days = st.select_slider("데이터 범위 (일, 0은 전체)", options=[0, 5, 10, 20])
    mode = st.radio("분석 방식", ["팀 단위", "라인업(선수) 단위"])

# [기능 2: 분석 모드 입력]
col1, col2 = st.columns(2)
if mode == "팀 단위":
    with col1: h_input = st.text_input("홈 팀명")
    with col2: a_input = st.text_input("원정 팀명")
    h_val, a_val = 50.0, 50.0 # 실제 데이터 연결 시 get_score 로직으로 대체 가능
else:
    with col1: 
        h_lineup = st.text_area("홈 라인업 (쉼표 구분)")
        h_pitcher = st.text_input("원정 선발 투수")
    with col2: 
        a_lineup = st.text_area("원정 라인업 (쉼표 구분)")
        a_pitcher = st.text_input("홈 선발 투수")
    h_val, a_val = 60.0, 55.0 # 실제 라인업 분석 로직 결과값 대입

# [기능 3: 분석 실행]
if st.button("최종 분석 실행"):
    prob, h_sim, a_sim = run_full_analysis(mode, h_val, a_val, selected_date, days)
    
    st.subheader(f"📊 승리 확률 예측: {prob*100:.2f}%")
    
    fig, ax = plt.subplots()
    ax.hist(h_sim, bins=50, alpha=0.5, label="Home")
    ax.hist(a_sim, bins=50, alpha=0.5, label="Away")
    ax.legend()
    st.pyplot(fig)
    st.caption("※ 홈 어드밴티지(4%) 및 환경 변수가 내부적으로 자동 반영되었습니다.")
