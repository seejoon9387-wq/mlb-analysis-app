import streamlit as st
import pandas as pd
import datetime
import os
import numpy as np

# --- 1. 백엔드: 데이터 정제 및 고도화된 시뮬레이션 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path): return None
    df = pd.read_csv(file_path)
    
    # [정제 및 피처 생성]
    df['batter_team'] = np.where(df['inning_topbot'] == 'top', df['away_team'], df['home_team'])
    df['pitcher_team'] = np.where(df['inning_topbot'] == 'top', df['home_team'], df['away_team'])
    
    # 최빈값 매핑 및 정제
    pitcher_map = df.groupby('pitcher')['pitcher_team'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    df['pitcher_2026_team'] = df['pitcher'].map(pitcher_map)
    df['is_whiff'] = df['is_whiff'].fillna(0)
    
    return df

def run_advanced_simulation(home, away, iterations=100000):
    df = get_processed_data()
    # [고도화된 피처 계산] 헛스윙률 기반 전력 지표 추출
    pitcher_stats = df.groupby('pitcher_2026_team')['is_whiff'].mean()
    
    home_whiff = pitcher_stats.get(home, 0.25) # 기본값 0.25
    away_whiff = pitcher_stats.get(away, 0.25)
    
    # 헛스윙률 차이를 기반으로 승리 확률 계산
    win_count = 0
    for _ in range(iterations):
        # 헛스윙 능력이 높을수록 승리 확률이 높게 설계
        if np.random.normal(home_whiff, 0.05) > np.random.normal(away_whiff, 0.05):
            win_count += 1
    return win_count / iterations

# --- 2. 프론트엔드: 메인 UI ---
st.title("⚾ MLB 승부 예측 분석기")

home_team = st.text_input("홈 팀 (예: BOS)")
away_team = st.text_input("원정 팀 (예: NYY)")

if st.button("분석 실행"):
    with st.spinner("헛스윙률 지표를 반영하여 시뮬레이션 중..."):
        try:
            prob = run_advanced_simulation(home_team, away_team)
            
            st.subheader("📊 헛스윙률 기반 예측 결과")
            col1, col2 = st.columns(2)
            col1.metric(f"{home_team} 승리 확률", f"{prob*100:.2f}%")
            col2.metric(f"{away_team} 승리 확률", f"{(1-prob)*100:.2f}%")
            
        except Exception as e:
            st.error("분석 실패: 팀 이름이 데이터셋에 존재하는지 확인하세요.")
