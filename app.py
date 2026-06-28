import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
import time, random, requests, os
from io import StringIO

# 1. 차단 방지형 안전 수집 엔진
def collect_safe_data():
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://baseballsavant.mlb.com/"}
    session = requests.Session()
    url = "https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats?year=2026&csv=true"
    try:
        response = session.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            df.to_csv('mlb_safe_data.csv', index=False)
            return df
    except: return None

# 2. 통계적 승리 기여도 분석 엔진
def run_victory_impact_analysis(df):
    df_clean = df.select_dtypes(include=[np.number]).dropna()
    features = [c for c in ['whiff_percent', 'pitch_velocity', 'spin_rate'] if c in df_clean.columns]
    
    if len(features) > 1:
        X = df_clean[features]
        y = df_clean.iloc[:, 0] # 타겟 지표
        model = LinearRegression().fit(X, y)
        return pd.DataFrame({'Indicator': features, 'Victory_Impact': model.coef_})
    return pd.DataFrame()

# 3. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 안전 데이터 수집 및 승리 진단 v17.1")

if st.sidebar.button("안전 모드 데이터 동기화 및 분석"):
    with st.spinner("서버 차단 우회 데이터 수집 및 회귀 모델 연산 중..."):
        df = collect_safe_data()
        if df is not None:
            analytics = run_victory_impact_analysis(df)
            
            st.subheader("📌 데이터 기반 승리 기여도 진단")
            st.dataframe(analytics)
            
            fig = px.bar(analytics, x='Indicator', y='Victory_Impact', color='Victory_Impact')
            st.plotly_chart(fig, use_container_width=True)
            
            st.success("시스템 정상 작동: 안전한 데이터 기반 진단이 완료되었습니다.")
        else:
            st.error("데이터 수집 실패. 네트워크 환경을 확인하세요.")
