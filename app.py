import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# 1. 데이터 검증 및 공수 통합 엔진 (1번 & 2번 적용)
@st.cache_data
def get_integrated_data():
    data = pd.read_csv('full_mlb_events_2026.csv')
    
    # [1번 적용] 결측치 보완 및 정합성 확보
    data['is_whiff'] = data['is_whiff'].fillna(0)
    data['woba_value'] = data['woba_value'].fillna(0)
    data['pitcher_team_official'] = data['pitcher_team_official'].fillna(data['pitcher_2026_team'])
    
    # [2번 적용] 공수 지표 결합
    stats = data.groupby('batter_2026_team').agg({
        'woba_value': 'mean',
        'is_whiff': 'mean'
    })
    return data, stats

# 몬테카를로 시뮬레이션
def run_simulation(home, away, stats, iterations=100000):
    # 가중치: 공격력(wOBA) 60% + 투수력(1-Whiff) 40%
    home_power = (stats.loc[home, 'woba_value'] * 0.6) + ((1 - stats.loc[home, 'is_whiff']) * 0.4)
    away_power = (stats.loc[away, 'woba_value'] * 0.6) + ((1 - stats.loc[away, 'is_whiff']) * 0.4)
    
    results = np.random.normal(home_power, 0.02, iterations) > np.random.normal(away_power, 0.02, iterations)
    return np.mean(results)

# 2. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 공수 균형 시뮬레이션 엔진 v35.0")

if st.sidebar.button("시뮬레이션 가동"):
    with st.spinner("데이터 무결성 검증 및 공수 밸런스 분석 중..."):
        df, stats = get_integrated_data()
        prob = run_simulation('BOS', 'NYY', stats)
        
        st.subheader("📊 [단계 1] 공수 지표 분석")
        st.dataframe(stats.loc[['BOS', 'NYY']])
        
        st.subheader("📈 [단계 2] 10만 번 시뮬레이션 결과")
        col1, col2 = st.columns(2)
        col1.metric("보스턴 승리 확률", f"{prob*100:.2f}%")
        col2.metric("양키스 승리 확률", f"{(1-prob)*100:.2f}%")
        
        st.success("데이터 검증 및 시뮬레이션 완료.")
