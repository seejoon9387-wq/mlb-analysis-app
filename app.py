import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# --- 1. 백엔드: 전력 통합 및 최근 데이터 분석 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path): return None
    df = pd.read_csv(file_path)
    
    # 데이터 정제 및 날짜 처리
    df['game_date'] = pd.to_datetime(df['game_date'])
    df['batter_team'] = np.where(df['inning_topbot'] == 'top', df['away_team'], df['home_team'])
    
    # 전력 지표 통합 (공격력 및 투구력 복합)
    # whiff_rate는 낮을수록 좋으나 공격력과 섞을 땐 방향성 조정 필요
    df['is_whiff'] = df['is_whiff'].fillna(0)
    df['launch_speed'] = df['launch_speed'].fillna(df['launch_speed'].mean())
    return df

def run_simulation(home, away, iterations=100000):
    df = get_processed_data()
    # 최근 10경기 데이터만 필터링 (데이터 범위 보완)
    recent_df = df[df['game_date'] >= df['game_date'].max() - pd.Timedelta(days=10)]
    
    # 전력 지표 통합: (타구 속도 - 헛스윙률) 기반 종합 전력 산출
    stats = recent_df.groupby('batter_team').agg({'launch_speed': 'mean', 'is_whiff': 'mean'})
    stats['power_index'] = stats['launch_speed'] - (stats['is_whiff'] * 100)
    
    home_val = stats.get(home, stats['power_index'].mean())
    away_val = stats.get(away, stats['power_index'].mean())
    
    # 시뮬레이션 및 데이터 분포 생성
    home_sim = np.random.normal(home_val, 5, iterations)
    away_sim = np.random.normal(away_val, 5, iterations)
    
    win_prob = np.mean(home_sim > away_sim)
    return win_prob, home_sim, away_sim

# --- 2. 프론트엔드: 메인 UI ---
st.title("⚾ MLB 승부 예측 분석기 (Advanced)")

home_team = st.text_input("홈 팀 (예: BOS)")
away_team = st.text_input("원정 팀 (예: NYY)")

if st.button("종합 분석 실행"):
    with st.spinner("최근 10경기 데이터로 시뮬레이션 중..."):
        prob, h_sim, a_sim = run_simulation(home_team, away_team)
        
        # 결과 출력
        col1, col2 = st.columns(2)
        col1.metric(f"{home_team} 승리", f"{prob*100:.1f}%")
        col2.metric(f"{away_team} 승리", f"{(1-prob)*100:.1f}%")
        
        # 데이터 분포 시각화 (시각화 보완)
        st.subheader("📊 승리 확률 분포")
        fig, ax = plt.subplots()
        ax.hist(h_sim, bins=50, alpha=0.5, label=f"{home_team}")
        ax.hist(a_sim, bins=50, alpha=0.5, label=f"{away_team}")
        ax.legend()
        st.pyplot(fig)
        

[Image of probability density distribution graph]
