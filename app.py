import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# (기존 NAME_MAP, get_mlb_schedule은 그대로 유지)

@st.cache_data
def get_prediction(home, away, master_df):
    # 1. 홈팀과 원정팀의 과거 데이터 필터링
    h_data = master_df[master_df['team'] == home]
    a_data = master_df[master_df['team'] == away]
    
    # 2. 데이터가 없을 경우 기본값 50% 반환
    if h_data.empty or a_data.empty: return 50
    
    # 3. 간단한 예측 알고리즘: '최근 득점(score)'의 평균을 비교하여 승률 산출
    h_avg = h_data['score'].mean()
    a_avg = a_data['score'].mean()
    
    # 승률 계산: (홈팀 득점력 / (홈팀+원정팀 득점력)) * 100
    win_rate = (h_avg / (h_avg + a_avg)) * 100
    return round(win_rate, 1)

# AI 승패 예측 메뉴 로직만 수정
elif menu == "AI 승패 예측":
    st.subheader("오늘의 경기 승률 예측 (데이터 기반)")
    if st.button("예측 분석 실행"):
        schedule = get_mlb_schedule()
        master_df = pd.read_csv('https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t')
        
        results = []
        for game in schedule:
            h = game['홈팀']
            a = game['원정팀']
            prob = get_prediction(h, a, master_df)
            results.append({"홈팀": h, "원정팀": a, "홈팀 승리 확률": f"{prob}%"})
            
        st.table(pd.DataFrame(results))
