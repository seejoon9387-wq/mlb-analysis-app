import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime

# --- 1. 유틸리티 및 팀 매핑 ---
def get_team_id_by_name(input_name):
    team_db = {
        '볼티': 'BAL', '양키스': 'NYY', '보스턴': 'BOS', '다저스': 'LAD', '메츠': 'NYM',
        '필리스': 'PHI', '컵스': 'CHC', '화이트삭스': 'CWS', '클리블랜드': 'CLE', '휴스턴': 'HOU'
    }
    return team_db.get(input_name, input_name)

# --- 2. 데이터 엔진 ---
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

# --- 3. 시뮬레이션 엔진 (환경 변수 자동 적용) ---
def run_simulation(mode, target_a, target_b, selected_date, days, iterations=100000):
    df = get_processed_data()
    
    if days > 0:
        target_date = pd.to_datetime(selected_date)
        df = df[(df['game_date'] <= target_date) & (df['game_date'] >= target_date - pd.Timedelta(days=days))]
    
    group_col = 'pitcher_team' if mode == "팀 단위" else 'pitcher'
    stats = df.groupby(group_col).agg({'release_speed': 'mean', 'is_strikeout': 'mean', 'is_whiff': 'mean'})
    
    def get_raw_score(name):
        s = stats.loc[name] if name in stats.index else pd.Series({'release_speed': 90, 'is_strikeout': 0.2, 'is_whiff': 0.2})
        return (s['release_speed'] * 0.3) + (s['is_strikeout'] * 100 * 0.4) + (s['is_whiff'] * 100 * 0.3)

    # 환경 변수 가중치 (내부 연산)
    # 실제 데이터에서 날씨/시간 정보를 가져올 수 없다면, 기본값 적용 및 통계적 가중치 반영
    home_field_advantage = 1.04 # 홈 팀 기본 우위
    night_game_bonus = 1.02     # 야간 경기 타자 유리 가정
    
    score_a = get_raw_score(target_a) * home_field_advantage
    score_b = get_raw_score(target_b) * night_game_bonus
    
    sim_a = np.random.normal(score_a, 3, iterations)
    sim_b = np.random.normal(score_b, 3, iterations)
    
    return np.mean(sim_a > sim_b), sim_a, sim_b

# --- 4. 프론트엔드 ---
st.title("⚾ MLB 종합 승부 예측 분석기")

mode = st.radio("분석 기준 선택", ["팀 단위", "투수 단위"], horizontal=True)

col1, col2 = st.columns(2)
with col1: selected_date = st.date_input("경기 날짜", datetime.date(2026, 6, 27))
with col2: days = st.select_slider("데이터 범위 (일, 0은 전체)", options=[0, 5, 10, 20])

input_a = st.text_input("홈 팀 또는 투수명")
input_b = st.text_input("원정 팀 또는 투수명")

if st.button("최종 분석 실행"):
    with st.spinner("환경 변수 및 최근 지표 종합 분석 중..."):
        try:
            target_a = get_team_id_by_name(input_a) if mode == "팀 단위" else input_a
            target_b = get_team_id_by_name(input_b) if mode == "팀 단위" else input_b
            
            prob, h_sim, a_sim = run_simulation(mode, target_a, target_b, selected_date, days)
            
            st.subheader(f"📊 {input_a} 승리 확률: {prob*100:.2f}%")
            
            fig, ax = plt.subplots()
            ax.hist(h_sim, bins=50, alpha=0.5, label=input_a)
            ax.hist(a_sim, bins=50, alpha=0.5, label=input_b)
            ax.legend()
            st.pyplot(fig)
            
            st.caption("※ 홈 이점(4%)과 야간 경기 가중치(2%)가 내부적으로 자동 반영되었습니다.")
        except Exception as e:
            st.error(f"데이터를 찾을 수 없습니다: {e}")
