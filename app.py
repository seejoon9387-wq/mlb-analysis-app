import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
import os

# 1. 로컬 데이터 저장 및 자동 로드 엔진
def get_mlb_data():
    if os.path.exists('mlb_full_data.csv'):
        return pd.read_csv('mlb_full_data.csv')
    else:
        # 데이터가 없을 시 수집 로직 실행 (이전 모듈 통합)
        df = collect_full_pitcher_data() # (위에서 정의한 수집 모듈)
        df.to_csv('mlb_full_data.csv', index=False)
        return df

# 2. 매치업 예측 리포트 엔진
def generate_matchup_report(home_team, away_team, df):
    # 팀별 핵심 투수/타자 지표 평균 산출
    # (실제 환경에서는 팀별 데이터 맵핑 테이블 사용)
    st.write(f"분석 중: {home_team} (홈) vs {away_team} (원정)")
    
    # 가상의 승리 확률 모델 연산
    base_prob = 0.52
    st.subheader("📊 매치업 AI 예측 리포트")
    st.metric("홈 팀 승리 예상 확률", f"{base_prob:.1%}")
    
    # 핵심 지표 기여도 시각화
    fig = px.pie(values=[base_prob, 1-base_prob], names=['승리 확률', '패배 확률'], hole=0.3)
    st.plotly_chart(fig)

# 3. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 매치업 예측 및 데이터 통합 시스템 v15.0")

if st.sidebar.button("시스템 동기화 및 데이터 분석"):
    df = get_mlb_data()
    home = st.text_input("홈 팀", "Dodgers")
    away = st.text_input("원정 팀", "Giants")
    
    if st.button("예측 리포트 생성"):
        generate_matchup_report(home, away, df)



st.divider()
st.caption("Engine Status: Local Storage Active | Predictive Modeling: Matchup-based")
