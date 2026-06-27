import streamlit as st
import pandas as pd
import datetime
import os
import numpy as np

# --- 1. 백엔드: 시뮬레이션 및 분석 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path): return None
    df = pd.read_csv(file_path)
    
    # [정제 로직 통합]
    df['batter_team'] = np.where(df['inning_topbot'] == 'top', df['away_team'], df['home_team'])
    df['pitcher_team'] = np.where(df['inning_topbot'] == 'top', df['home_team'], df['away_team'])
    cols_to_fill = ['launch_speed', 'is_whiff', 'release_speed']
    for col in cols_to_fill:
        if col in df.columns: df[col] = df[col].fillna(0)
    return df

def run_advanced_simulation(home, away, iterations=100000):
    # 실제 시뮬레이션 로직: 데이터 평균을 기반으로 확률 계산
    # (예시: 팀 평균 지표를 활용한 간단한 가중치 확률 모델)
    df = get_processed_data()
    home_data = df[df['home_team'] == home]['release_speed'].mean()
    away_data = df[df['away_team'] == away]['release_speed'].mean()
    
    # 몬테카를로 시뮬레이션 기초 로직
    win_count = 0
    for _ in range(iterations):
        if np.random.normal(home_data, 5) > np.random.normal(away_data, 5):
            win_count += 1
    return win_count / iterations

# --- 2. 프론트엔드: 메인 UI ---
st.title("⚾ MLB 승부 예측 분석기")

home_team = st.text_input("홈 팀 (예: BOS)")
away_team = st.text_input("원정 팀 (예: NYY)")

if st.button("분석 실행"):
    with st.spinner("10만 번의 시뮬레이션을 수행 중입니다..."):
        try:
            bos_win_prob = run_advanced_simulation(home_team, away_team)
            
            st.subheader("📊 10만 번 시뮬레이션 결과")
            col1, col2 = st.columns(2)
            col1.metric(f"{home_team} 승리 확률", f"{bos_win_prob*100:.2f}%")
            col2.metric(f"{away_team} 승리 확률", f"{(1-bos_win_prob)*100:.2f}%")
            
        except Exception as e:
            st.error("분석 실패: 데이터가 부족하거나 팀 이름을 다시 확인하세요.")
