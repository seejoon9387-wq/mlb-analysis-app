import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime

# --- 1. 유틸리티: 팀 ID 매핑 ---
def get_team_id_by_name(input_name):
    team_db = {
        '볼티': 'BAL', '양키스': 'NYY', '보스턴': 'BOS', '다저스': 'LAD', '메츠': 'NYM',
        '필리스': 'PHI', '컵스': 'CHC', '화이트삭스': 'CWS', '클리블랜드': 'CLE', '휴스턴': 'HOU'
    }
    return team_db.get(input_name, input_name)

# --- 2. 백엔드: 데이터 로드 및 정제 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path): return None
    df = pd.read_csv(file_path)
    df['game_date'] = pd.to_datetime(df['game_date'])
    
    # 지표 정제
    df['is_strikeout'] = df['events'].apply(lambda x: 1 if x == 'strikeout' else 0)
    cols = ['release_speed', 'launch_speed', 'is_whiff', 'is_strikeout']
    for col in cols:
        if col in df.columns: df[col] = df[col].fillna(0)
    return df

# --- 3. 고도화된 시뮬레이션 엔진 ---
def run_advanced_simulation(home, away, selected_date, days, iterations=100000):
    df = get_processed_data()
    home, away = get_team_id_by_name(home), get_team_id_by_name(away)
    
    # 선택된 날짜와 데이터 범위 필터링
    target_date = pd.to_datetime(selected_date)
    recent_df = df[(df['game_date'] <= target_date) & (df['game_date'] >= target_date - pd.Timedelta(days=days))]
    
    stats = recent_df.groupby('pitcher_team').agg({'release_speed': 'mean', 'is_strikeout': 'mean', 'is_whiff': 'mean'})
    
    def get_score(team):
        s = stats.loc[team] if team in stats.index else pd.Series({'release_speed': 90, 'is_strikeout': 0.2, 'is_whiff': 0.2})
        # 투구 지표(70%) + 타격 지표(30% 가중치 시뮬레이션)
        return (s['release_speed'] * 0.3) + (s['is_strikeout'] * 100 * 0.4) + (s['is_whiff'] * 100 * 0.3)

    h_score, a_score = get_score(home), get_score(away)
    
    h_sim = np.random.normal(h_score, 3, iterations)
    a_sim = np.random.normal(a_score, 3, iterations)
    
    prob = np.mean(h_sim > a_sim)
    return prob, h_sim, a_sim

# --- 4. 프론트엔드 UI ---
st.title("⚾ MLB 종합 승부 예측 분석기")

col1, col2 = st.columns(2)
with col1: selected_date = st.date_input("경기 날짜", datetime.date(2026, 6, 27))
with col2: days = st.select_slider("최근 데이터 범위 (일)", options=[5, 10, 20])

home_input = st.text_input("홈 팀")
away_input = st.text_input("원정 팀")

if st.button("최종 분석 실행"):
    with st.spinner("최근 투수 지표 및 데이터 종합 분석 중..."):
        try:
            prob, h_sim, a_sim = run_advanced_simulation(home_input, away_input, selected_date, days)
            
            st.subheader(f"📊 {home_input} 승리 확률: {prob*100:.2f}%")
            
            fig, ax = plt.subplots()
            ax.hist(h_sim, bins=50, alpha=0.5, label="Home")
            ax.hist(a_sim, bins=50, alpha=0.5, label="Away")
            ax.legend()
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}. 팀 이름을 다시 확인해 주세요.")
