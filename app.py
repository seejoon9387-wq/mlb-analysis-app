import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# --- 1. 백엔드: 공수 통합 분석 엔진 ---
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

def run_balanced_simulation(home, away, iterations=100000):
    df = get_processed_data()
    recent_df = df[df['game_date'] >= df['game_date'].max() - pd.Timedelta(days=10)]
    
    # 팀별 지표 그룹화
    stats = recent_df.groupby('batter_team').agg({'launch_speed': 'mean', 'is_whiff': 'mean'})
    
    # 공수 지수 계산 (투수 헛스윙은 높을수록 좋고, 상대 타자 타구 속도는 낮을수록 좋음)
    # Power Index = (우리 팀 타구 속도) - (우리 팀 투수 헛스윙률 * 100)
    # 간단한 공수 밸런스 모델 적용
    h_launch = stats.loc[home, 'launch_speed'] if home in stats.index else 90
    h_whiff = stats.loc[home, 'is_whiff'] if home in stats.index else 0.25
    a_launch = stats.loc[away, 'launch_speed'] if away in stats.index else 90
    a_whiff = stats.loc[away, 'is_whiff'] if away in stats.index else 0.25
    
    home_score = (h_launch * 0.4) + (h_whiff * 60) # 타격 40% + 투구 60% 가중치
    away_score = (a_launch * 0.4) + (a_whiff * 60)
    
    home_sim = np.random.normal(home_score, 5, iterations)
    away_sim = np.random.normal(away_score, 5, iterations)
    
    prob = np.mean(home_sim > away_sim)
    return prob, home_sim, away_sim

# --- 2. 프론트엔드: 메인 UI ---
st.title("⚾ 공수 밸런스 기반 MLB 승부 예측기")

home_team = st.text_input("홈 팀 (예: BOS)")
away_team = st.text_input("원정 팀 (예: NYY)")

if st.button("종합 분석 실행"):
    with st.spinner("공격력과 투구 지표를 종합 분석 중..."):
        try:
            prob, h_sim, a_sim = run_balanced_simulation(home_team, away_team)
            
            st.subheader("📊 종합 분석 결과")
            col1, col2 = st.columns(2)
            col1.metric("홈 팀 승리 확률", f"{prob*100:.2f}%")
            col2.metric("원정 팀 승리 확률", f"{(1-prob)*100:.2f}%")
            
            st.subheader("📊 전력 밸런스 분포")
            fig, ax = plt.subplots()
            ax.hist(h_sim, bins=50, alpha=0.6, label=f"{home_team} (Balanced)")
            ax.hist(a_sim, bins=50, alpha=0.6, label=f"{away_team} (Balanced)")
            ax.legend()
            st.pyplot(fig)
            
        except Exception as e:
            st.error("분석 실패: 팀 데이터가 부족합니다.")
