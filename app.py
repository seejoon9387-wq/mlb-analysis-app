import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# --- 1. 데이터 처리 및 선수 스탯 조회 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path): return None
    df = pd.read_csv(file_path)
    return df

def get_player_stats(player_name, df):
    # 선수별 평균 타구 속도를 전력 지수로 사용
    player_data = df[df['batter'] == player_name]
    return player_data['launch_speed'].mean() if not player_data.empty else 88.0

# --- 2. 라인업 분석 엔진 ---
def analyze_custom_lineup(team_name, lineup, pitcher, df):
    # 선수별 스탯 매핑 및 평균 전력 점수 산출
    scores = [get_player_stats(p, df) for p in lineup]
    avg_power = sum(scores) / len(scores) if scores else 0
    
    # 투수 억제력 반영 (특정 투수 대상 상성)
    pitcher_data = df[df['pitcher'] == pitcher]
    whiff_vs_pitcher = pitcher_data['is_whiff'].mean() if 'is_whiff' in pitcher_data.columns else 0.2
    
    # 최종 매치업 점수: 타선 전력 - (투수 억제력 보정)
    final_score = avg_power - (whiff_vs_pitcher * 50)
    return final_score

# --- 3. 프론트엔드 ---
st.title("⚾ 라인업 기반 매치업 시뮬레이터")

df = get_processed_data()

col1, col2 = st.columns(2)
with col1:
    team_name = st.text_input("팀명 (예: Boston Red Sox)")
    lineup_input = st.text_area("라인업 입력 (쉼표로 구분)", "Rafael Devers, Triston Casas, Jarren Duran")
with col2:
    opp_pitcher = st.text_input("상대 선발 투수명")

if st.button("라인업 분석 실행"):
    lineup = [p.strip() for p in lineup_input.split(',')]
    score = analyze_custom_lineup(team_name, lineup, opp_pitcher, df)
    
    st.subheader(f"📊 {team_name}의 {opp_pitcher} 공략 예상 점수: {score:.2f}")
    
    st.write("### 분석 상세:")
    st.info(f"- 참여 선수 수: {len(lineup)}명")
    st.write(f"- 상대 투수 헛스윙 유도율(최근): {df[df['pitcher']==opp_pitcher]['is_whiff'].mean():.2%}")
    
    # 시각화: 예상 라인업 전력 분포
    fig, ax = plt.subplots()
    ax.bar(lineup, [get_player_stats(p, df) for p in lineup], color='skyblue')
    plt.xticks(rotation=45)
    plt.ylabel("평균 타구 속도 (mph)")
    st.pyplot(fig)
