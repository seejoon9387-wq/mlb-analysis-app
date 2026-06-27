import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from io import StringIO
import requests
from bs4 import BeautifulSoup
import time

# 1. 고밀도 데이터 수집 엔진 (Savant 직접 크롤링)
@st.cache_data
def collect_full_savant_data():
    metrics_map = {'expected_statistics': 'expected-statistics', 'run_value': 'run-value'}
    all_data = []
    for year in [2024, 2025, 2026]:
        for name, url_part in metrics_map.items():
            url = f"https://baseballsavant.mlb.com/leaderboard/{url_part}?year={year}&min=0&csv=true"
            try:
                response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
                if response.status_code == 200:
                    df = pd.read_csv(StringIO(response.text))
                    df['Metric'], df['Year'] = name, year
                    all_data.append(df)
            except: continue
            time.sleep(0.5)
    return pd.concat(all_data, ignore_index=True)

# 2. 실시간 외부 변수(뉴스) 보정 엔진
def get_news_sentiment_impact(team_name):
    url = f"https://www.google.com/search?q={team_name}+mlb+news&tbm=nws"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, "html.parser")
    news_text = " ".join([item.get_text() for item in soup.select("div.SoaBEf")])
    # 부상/이슈 키워드 기반 승률 가중치 보정
    impact = -0.07 if any(k in news_text.lower() for k in ["injury", "out", "suspension", "bad"]) else 0.02
    return impact

# 3. 메인 분석 엔진
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 정밀 예측 및 객관적 분석 엔진 v11.0")

if st.sidebar.button("분석 실행 (데이터 수집+학습+뉴스보정)"):
    with st.spinner("최신 데이터 수집 및 AI 모델 연산 중..."):
        # 데이터 수집
        df = collect_full_savant_data()
        df_num = df.select_dtypes(include=[np.number]).dropna()
        
        # 머신러닝 중요도 분석
        X = df_num.drop(columns=['Year'], errors='ignore')
        y = df_num.iloc[:, 0]
        model = RandomForestRegressor().fit(X, y)
        
        # 결과값 도출
        importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_}).sort_values(by='Importance', ascending=False)
        
        # 시각화
        st.subheader("📊 객관적 중요도 (Feature Importance)")
        fig = px.bar(importance.head(10), x='Importance', y='Feature', orientation='h', color='Importance')
        st.plotly_chart(fig, use_container_width=True)
        
        # 뉴스 보정 결과
        news_impact = get_news_sentiment_impact("Dodgers")
        st.metric("실시간 이슈 뉴스 보정치", f"{news_impact:+.2%}")


st.divider()
st.caption("Engine Status: Savant Metrics + News Sentiment Integration Active")
