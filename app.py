import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime

# --- 1. 데이터 처리 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path): return None
    df = pd.read_csv(file_path)
    df['game_date'] = pd.to_datetime(df['game_date'])
    # 필요한 컬럼 정리
    for col in ['release_speed', 'launch_speed', 'is_whiff']:
        if col in df.columns: df[col] = df[col].fillna(0)
    return df

# --- 2. 상성 추적 시뮬레이션 엔진 ---
def run_matchup_stats(team, pitcher, selected_date, days):
    df = get_processed_data()
    
    # 1. 기간 필터링
    if days > 0:
        target_date = pd.to_datetime(selected_date)
        df = df[(df['game_date'] <= target_date) & (df['game_date'] >= target_date - pd.Timedelta(days=days))]
    
    # 2. 핵심 로직: [해당 팀]이 [해당 투수]를 상대했을 때의 데이터만 추출
    matchup_df = df[(df['batter_team'] == team) & (df['pitcher'] == pitcher)]
    
    if matchup_df.empty:
        return None # 데이터 없음
        
    # 상성 통계 산출
    stats = {
        'avg_launch_speed': matchup_df['launch_speed'].mean(),
        'whiff_rate_vs_pitcher': matchup_df['is_whiff'].mean()
    }
    return stats

# --- 3. 프론트엔드 ---
st.title("⚾ 팀 vs 특정 선발 상성 분석기")

col1, col2 = st.columns(2)
with col1:
    h_team = st.text_input("홈 팀명")
    a_pitcher = st.text_input("원정 선발 투수명")
with col2:
    a_team = st.text_input("원정 팀명")
    h_pitcher = st.text_input("홈 선발 투수명")

selected_date = st.date_input("경기 날짜", datetime.date(2026, 6, 27))
days = st.select_slider("데이터 추적 기간 (0은 전체)", options=[0, 5, 10, 20])

if st.button("상성 분석 실행"):
    with st.spinner("과거 기록을 추적하여 상성 데이터를 추출 중..."):
        # 양쪽의 상성 데이터 추출
        home_vs_away_p = run_matchup_stats(h_team, a_pitcher, selected_date, days)
        away_vs_home_p = run_matchup_stats(a_team, h_pitcher, selected_date, days)
        
        if home_vs_away_p and away_vs_home_p:
            st.subheader("📊 상성 매치업 결과")
            # 간단한 점수 산출
            home_score = (home_vs_away_p['avg_launch_speed'] * 0.5) - (home_vs_away_p['whiff_rate_vs_pitcher'] * 50)
            away_score = (away_vs_home_p['avg_launch_speed'] * 0.5) - (away_vs_home_p['whiff_rate_vs_pitcher'] * 50)
            
            prob = home_score / (home_score + away_score)
            st.metric(f"{h_team}의 {a_pitcher} 공략 확률", f"{prob*100:.2f}%")
            
            st.write(f"📈 {h_team} vs {a_pitcher} 평균 타구 속도: {home_vs_away_p['avg_launch_speed']:.2f} mph")
            st.write(f"📉 {h_team} vs {a_pitcher} 헛스윙률: {home_vs_away_p['whiff_rate_vs_pitcher']:.2%}")
        else:
            st.warning("선택한 기간 동안 해당 팀과 투수의 맞대결 기록이 없습니다.")
