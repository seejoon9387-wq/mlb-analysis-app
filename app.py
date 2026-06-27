import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import requests
from bs4 import BeautifulSoup

# 1. 외부 뉴스 검색 보정 (객관적 정보 수집)
def get_realtime_news_impact(team_name):
    """Google News에서 팀 관련 실시간 이슈(부상 등)를 파싱하여 가중치 도출"""
    url = f"https://www.google.com/search?q={team_name}+mlb+news&tbm=nws"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    # 간단한 키워드 기반 부정적 이슈(부상 등) 탐색 예시
    news = [item.get_text() for item in soup.select("div.SoaBEf")]
    impact = -0.05 if any("injury" in n.lower() or "out" in n.lower() for n in news) else 0
    return impact

# 2. AI 연산 및 시각화 엔진
def run_full_analysis(df):
    X = df.select_dtypes(include=[np.number])
    y = df['WinRate'] # 가정된 타겟 컬럼
    model = RandomForestRegressor().fit(X, y)
    
    # 중요도 추출
    importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_})
    return importance.sort_values(by='Importance', ascending=False)

# 3. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 객관적 정밀 예측 엔진 v10.0")

if st.sidebar.button("분석 실행"):
    # 가상 데이터 로드 (실제 데이터 파이프라인 연동 부분)
    df = pd.DataFrame({'WinRate': np.random.rand(10), 'ERA': np.random.rand(10), 'OPS': np.random.rand(10)})
    
    # 1. 중요도 분석
    imp = run_full_analysis(df)
    st.subheader("📊 객관적 판단 기준(Importance)")
    fig = px.bar(imp, x='Importance', y='Feature', orientation='h')
    st.plotly_chart(fig)
    
    # 2. 뉴스 보정
    news_impact = get_realtime_news_impact("Dodgers")
    st.info(f"실시간 뉴스 보정 적용: {news_impact:.2%}")

st.caption("Status: Integrated Feature Importance & News Sentiment Analysis")
