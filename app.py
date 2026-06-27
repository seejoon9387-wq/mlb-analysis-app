import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime

# --- 1. 백엔드: 데이터 및 환경 변수 반영 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path): return None
    df = pd.read_csv(file_path)
    df['game_date'] = pd.to_datetime(df['game_date'])
    # 환경 데이터 보정 (데이터셋에 컬럼이 있다고 가정)
    # df['is_night'] = (df['game_time'] >= 18).astype(int)
    return df

def run_contextual_simulation(h_data, a_data, weather, time_of_day, iterations=100000):
    # 환경 변수 가중치 설정
    weather_factor = 1.05 if weather == "맑음" else 0.95
    time_factor = 1.03 if time_of_day == "야간" else 1.00
    home_field_advantage = 1.04 # 홈 이점

    # 점수 계산 시 환경 변수 반영
    score_home = h_data * home_field_advantage * weather_factor
    score_away = a_data * time_factor
    
    sim_home = np.random.normal(score_home, 2, iterations)
    sim_away = np.random.normal(score_away, 2, iterations)
    
    prob = np.mean(sim_home > sim_away)
    return prob, sim_home, sim_away

# --- 2. 프론트엔드 ---
st.title("⚾ MLB 종합 환경 변수 예측기")

# 환경 변수 입력 UI
with st.expander("경기 환경 설정"):
    weather = st.selectbox("날씨", ["맑음", "흐림", "비/바람"])
    time_of_day = st.selectbox("경기 시간", ["주간", "야간"])
    st.info("홈 팀은 4%의 필드 어드밴티지가 자동으로 적용됩니다.")

col1, col2 = st.columns(2)
with col1:
    h_team = st.text_input("홈 팀")
    h_val = st.number_input("홈 팀 전력 지수", value=50.0)
with col2:
    a_team = st.text_input("원정 팀")
    a_val = st.number_input("원정 팀 전력 지수", value=50.0)

if st.button("분석 실행"):
    prob, h_sim, a_sim = run_contextual_simulation(h_val, a_val, weather, time_of_day)
    
    st.subheader(f"📊 최종 승리 확률: {prob*100:.2f}%")
    
    fig, ax = plt.subplots()
    ax.hist(h_sim, bins=50, alpha=0.5, label=f"Home ({h_team})")
    ax.hist(a_sim, bins=50, alpha=0.5, label=f"Away ({a_team})")
    ax.legend()
    st.pyplot(fig)
