import streamlit as st
import requests
import pandas as pd
import datetime
import pytz
from io import StringIO

# 1. 설정
API_KEY = '9c3c5d2369ad9163a19c3e88dfa1f9c5'

# 2. 메인 화면
st.title("⚾ MLB 올인원 분석기")

# 탭 나누기
tab1, tab2 = st.tabs(["경기 배당 분석", "서번트 선수 지표 분석"])

# --- 탭 1: 경기 배당 분석 ---
with tab1:
    selected_date = st.date_input("경기 날짜 선택", datetime.date.today())
    home_team = st.text_input("홈 팀 이름 (예: Yankees)", "")
    away_team = st.text_input("원정 팀 이름 (예: Red Sox)", "")
    
    if st.button("배당 분석 실행"):
        if not home_team or not away_team:
            st.warning("팀 이름을 입력하세요!")
        else:
            url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
            params = {'apiKey': API_KEY, 'regions': 'us', 'markets': 'h2h', 'oddsFormat': 'decimal'}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                found = False
                kst = pytz.timezone('Asia/Seoul')
                for match in data:
                    match_dt_utc = datetime.datetime.fromisoformat(match['commence_time'].replace('Z', '+00:00'))
                    match_dt_kst = match_dt_utc.astimezone(kst)
                    if (selected_date == match_dt_kst.date()) and (home_team.lower() in match['home_team'].lower()):
                        st.success("경기 데이터를 찾았습니다!")
                        found = True
                        break
                if not found: st.error("해당 경기를 찾을 수 없습니다.")

# --- 탭 2: 서번트 선수 지표 분석 ---
with tab2:
    year = st.selectbox("연도 선택", [2024, 2025, 2026])
    metric = st.selectbox("지표 선택", ['statcast', 'expected_statistics', 'run_value', 'outs_above_average'])
    
    if st.button("지표 데이터 불러오기"):
        url = f"https://baseballsavant.mlb.com/leaderboard/{metric.replace('_', '-')}?year={year}&min=0&csv=true"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            st.dataframe(df.head(10))
        else:
            st.error("데이터를 가져올 수 없습니다.")
