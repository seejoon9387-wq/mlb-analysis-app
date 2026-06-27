import streamlit as st
import pandas as pd
import os
import requests
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier

# 1. AI 예측 모델링 (연산 엔진)
def run_ai_prediction(df):
    """과거 데이터를 학습하여 현재 승률(win_prob)을 예측"""
    # 단순화를 위해 승/패 기록을 기반으로 모델 학습
    # 실제 환경에서는 더 많은 변수(선발투수, 구장 등)를 여기서 연산
    X = df[['AwayScore', 'HomeScore']] # 예시 변수
    y = (df['Winner'] == df['Home']).astype(int) 
    model = RandomForestClassifier()
    model.fit(X, y)
    return model.predict_proba(X)[:, 1]

# 2. 메인 로직
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 정밀 예측 및 분석 대시보드")

files = [f for f in os.listdir('/content/') if f.endswith('.csv')]
selected_file = st.sidebar.selectbox("데이터 선택", files)

if selected_file:
    df = pd.read_csv(os.path.join('/content/', selected_file))
    
    if st.sidebar.button("AI 예측 가동"):
        # 승률 추론
        df['pred_win_prob'] = run_ai_prediction(df)
        # Edge 계산 (예시 배당 1.9)
        df['edge'] = (df['pred_win_prob'] / (1/1.9)) - 1
        
        # 3. 데이터 시각화
        st.subheader("📌 Edge 상위 팀 시각화")
        fig = px.bar(df.sort_values('edge', ascending=False).head(10), 
                     x='Home', y='edge', color='edge', title="저평가된 팀 분석")
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df[['Home', 'Away', 'pred_win_prob', 'edge']])

st.divider()
st.caption("AI Engine Status: Predictive Modeling Active | Visualize: Enabled")
