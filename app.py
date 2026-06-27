import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from io import StringIO
import requests
import time

# 1. 고밀도 데이터 수집 엔진 (Savant 직접 크롤링)
@st.cache_data
def collect_full_savant_data():
    metrics_map = {'expected_statistics': 'expected-statistics', 'run_value': 'run-value'}
    all_data = []
    for year in [2024, 2025, 2026]:
        for name, url_part in metrics_map.items():
            url = f"https://baseballsavant.mlb.com/leaderboard/{url_part}?year={year}&min=0&csv=true"
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                df = pd.read_csv(StringIO(response.text))
                df['Metric'], df['Year'] = name, year
                all_data.append(df)
            time.sleep(1)
    return pd.concat(all_data, ignore_index=True)

# 2. AI 연산 및 중요도 분석
def run_analysis(df):
    # 수치형 데이터만 선택하여 분석
    df_num = df.select_dtypes(include=[np.number]).dropna()
    X = df_num.drop(columns=['Year'], errors='ignore')
    y = df_num.iloc[:, 0] # 첫 번째 컬럼을 타겟으로 가정(추후 변경 가능)
    model = RandomForestRegressor().fit(X, y)
    
    importance = pd.DataFrame({'Feature': X.columns, 'Importance': model.feature_importances_})
    return importance.sort_values(by='Importance', ascending=False)

# 3. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 객관적 데이터 분석 엔진 (Savant 통합)")

if st.sidebar.button("데이터 수집 및 정밀 분석 시작"):
    with st.spinner("Savant에서 대규모 데이터 수집 중..."):
        full_df = collect_full_savant_data()
        st.success(f"총 {len(full_df)}건의 데이터 수집 완료")
        
        # 중요도 분석
        imp = run_analysis(full_df)
        
        st.subheader("📊 데이터 기반 객관적 중요도 (Feature Importance)")
        fig = px.bar(imp.head(15), x='Importance', y='Feature', orientation='h', color='Importance')
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(full_df.head(20))

st.caption("System Status: Savant Metrics Integrated | Predictive Engine: Active")
