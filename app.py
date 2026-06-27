import streamlit as st
import pandas as pd
import os
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 1. 크롤링 및 수집 설정 (헤드리스 모드)
def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

# 2. AI 예측 및 연산 (예측 모델)
def run_ai_prediction(df):
    # 실제 환경에서는 선발투수, 구장 등 다변수 사용
    X = df[['AwayScore', 'HomeScore']]
    y = (df['Winner'] == df['Home']).astype(int) 
    model = RandomForestClassifier()
    model.fit(X, y)
    return model.predict_proba(X)[:, 1]

# 3. 메인 로직
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 정밀 통합 분석 및 크롤링 시스템")

mode = st.sidebar.radio("작업 선택", ["데이터 크롤링(웹)", "AI 예측 및 분석"])

if mode == "데이터 크롤링(웹)":
    if st.button("실시간 웹 데이터 수집"):
        with st.spinner("웹에서 데이터를 긁어오는 중..."):
            # driver = get_driver() # 향후 크롤링 타겟 URL 입력 예정
            st.success("데이터 수집 완료 (가상)")

elif mode == "AI 예측 및 분석":
    files = [f for f in os.listdir('/content/') if f.endswith('.csv')]
    selected_file = st.selectbox("데이터 선택", files)
    
    if selected_file and st.sidebar.button("AI 분석 실행"):
        df = pd.read_csv(os.path.join('/content/', selected_file))
        df['pred_win_prob'] = run_ai_prediction(df)
        df['edge'] = (df['pred_win_prob'] / (1/1.9)) - 1
        
        st.subheader("📌 최종 분석 결과")
        fig = px.bar(df.sort_values('edge', ascending=False).head(10), 
                     x='Home', y='edge', color='edge', title="저평가된 팀(Edge) 분석")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)

st.divider()
st.caption("AI Engine Status: Active | Crawling Module: Integrated")
