import streamlit as st
import pandas as pd
import requests
from io import StringIO
import time

@st.cache_data(ttl=86400) # 데이터를 하루 동안 저장(캐싱)하여 속도 극대화
def get_savant_data(year, metric_type):
    # 매핑 데이터
    metrics_map = {
        'statcast': 'statcast', 'expected_statistics': 'expected-statistics', 
        'run_value': 'run-value', 'outs_above_average': 'outs-above-average'
    }
    url_part = metrics_map.get(metric_type, 'statcast')
    url = f"https://baseballsavant.mlb.com/leaderboard/{url_part}?year={year}&min=0&csv=true"
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    return pd.DataFrame()

# 웹 화면 (로그 확인용)
st.title("⚾ 베이스볼 서번트 분석기")
year = st.selectbox("연도 선택", [2024, 2025, 2026])
metric = st.selectbox("지표 선택", ['statcast', 'expected_statistics', 'run_value', 'outs_above_average'])

if st.button("데이터 분석 시작"):
    with st.spinner("서번트에서 데이터를 불러오는 중..."):
        df = get_savant_data(year, metric)
        if not df.empty:
            st.success(f"데이터 {len(df)}건 확보!")
            st.dataframe(df.head(10)) # 결과 미리보기
        else:
            st.error("데이터를 가져올 수 없습니다.")
