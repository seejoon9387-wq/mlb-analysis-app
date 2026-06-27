import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime

# --- 1. 백엔드: 데이터 로드 및 정제 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path): return None
    df = pd.read_csv(file_path)
    
    df['game_date'] = pd.to_datetime(df['game_date'])
    df['batter_team'] = np.where(df['inning_topbot'] == 'top', df['away_team'], df['home_team'])
    df['pitcher_team'] = np.where(df['inning_topbot'] == 'top', df['home_team'], df['away_team'])
    
    # 지표 정제
    df['is_whiff'] = df['is_whiff'].fillna(0)
    df['launch_speed'] = df['launch_speed'].fillna(df['launch_speed'].mean())
    return df

# --- 2. 시뮬레이션 엔진 (날짜 및 가중치 반영) ---
def run_balanced_simulation(home, away, selected_date, iterations=100000):
    df = get_processed_data()
    # 선택된 날짜 기준 10일 전까지의 데이터로 필터링
    target_date = pd.to_datetime(selected_date)
    recent_df = df[(df['game_date'] <= target_date) & (df['game_date'] >= target_date - pd.Timedelta(days=10))]
    
    stats = recent_df.groupby('batter_team').agg({'launch_speed': 'mean', 'is_whiff': 'mean'})
    
    def get_score(team):
        launch = stats.loc[team, 'launch_speed'] if team in stats.index else 90
        whiff = stats.loc[team, 'is_whiff'] if team in stats.index else 0.25
        return (launch * 0.5) + (whiff * 100 * 0.5)

    home_score = get_score(home)
    away_score = get_score(away)
    
    home_sim = np.random.normal(home_score, 5, iterations)
    away_sim = np.random.normal(away_score, 5, iterations)
    
    prob = np.mean(home_sim > away_sim)
    return prob, home_sim, away_sim

# --- 3. 프론트엔드: 메인 UI ---
st.title("⚾ MLB 승부 예측 분석기 (통합 완성형)")

# [누적 복구] 날짜 선택창 추가
selected_date = st.date_input("경기 날짜 선택", datetime.date(2026, 6, 27))
home_team = st.text_input("홈 팀 (예: BOS)")
away_team = st.text_input("원정 팀 (예: NYY)")

if st.button("최종 분석 실행"):
    with st.spinner("데이터 분석 및 시뮬레이션 중..."):
        try:
            prob, h_sim, a_sim = run_balanced_simulation(home_team, away_team, selected_date)
            
            st.subheader("📊 최종 보정된 승리 확률")
            st.metric(f"{home_team} 승리 확률", f"{prob*100:.2f}%")
            
            st.subheader("📊 전력 분포도")
            fig, ax = plt.subplots()
            ax.hist(h_sim, bins=50, alpha=0.5, label=f"{home_team}")
            ax.hist(a_sim, bins=50, alpha=0.5, label=f"{away_team}")
            ax.legend()
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}. 팀 이름이나 데이터 기간을 확인하세요.")
