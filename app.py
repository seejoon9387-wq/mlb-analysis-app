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

# --- 2. 데이터 처리 엔진 ---
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

# --- 3. 시뮬레이션 엔진 ---
def run_simulation(mode, target_a, target_b, selected_date, days, iterations=100000):
    df = get_processed_data()
    target_date = pd.to_datetime(selected_date)
    
    # 데이터 필터링 (기간)
    if days > 0:
        df = df[(df['game_date'] <= target_date) & (df['game_date'] >= target_date - pd.Timedelta(days=days))]
    
    # 모드별 그룹화 (팀 vs 투수)
    group_col = 'pitcher_team' if mode == "팀 단위" else 'pitcher'
    stats = df.groupby(group_col).agg({'release_speed': 'mean', 'is_strikeout': 'mean', 'is_whiff': 'mean'})
    
    def get_score(name):
        s = stats.loc[name] if name in stats.index else pd.Series({'release_speed': 90, 'is_strikeout': 0.2, 'is_whiff': 0.2})
        return (s['release_speed'] * 0.3) + (s['is_strikeout'] * 100 * 0.4) + (s['is_whiff'] * 100 * 0.3)

    score_a, score_b = get_score(target_a), get_score(target_b)
    sim_a = np.random.normal(score_a, 3, iterations)
    sim_b = np.random.normal(score_b, 3, iterations)
    
    prob = np.mean(sim_a > sim_b)
    return prob, sim_a, sim_b

# --- 4. 프론트엔드 ---
st.title("⚾ MLB 맞춤형 승부 예측 분석기")

# 모드 선택
mode = st.radio("분석 기준 선택", ["팀 단위", "투수 단위"], horizontal=True)

col1, col2 = st.columns(2)
with col1: selected_date = st.date_input("경기 날짜", datetime.date(2026, 6, 27))
with col2: days = st.select_slider("데이터 범위 (일, 0은 전체)", options=[0, 5, 10, 20])

if mode == "팀 단위":
    input_a = st.text_input("홈 팀명")
    input_b = st.text_input("원정 팀명")
    # 팀 ID 매핑
    target_a, target_b = get_team_id_by_name(input_a), get_team_id_by_name(input_b)
else:
    target_a = st.text_input("홈 선발 투수 이름")
    target_b = st.text_input("원정 선발 투수 이름")

if st.button("분석 실행"):
    with st.spinner("데이터 분석 중..."):
        try:
            prob, h_sim, a_sim = run_simulation(mode, target_a, target_b, selected_date, days)
            st.subheader(f"📊 {target_a} 승리 확률: {prob*100:.2f}%")
            
            fig, ax = plt.subplots()
            ax.hist(h_sim, bins=50, alpha=0.5, label=target_a)
            ax.hist(a_sim, bins=50, alpha=0.5, label=target_b)
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"데이터를 찾을 수 없습니다: {e}")
