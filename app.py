import streamlit as st
import statsapi
import pandas as pd
import requests
import os
from pybaseball import statcast

# --- 1. 설정 및 초기값 ---
st.set_page_config(page_title="MLB AI Analyst Pro", layout="wide")
st.title("⚾ MLB AI 정밀 통합 분석 시스템")

# 팀 명칭 매핑
TEAM_NAME_MAP = {
    'Los Angeles Dodgers': 'LAD', 'San Diego Padres': 'SD', 'Atlanta Braves': 'ATL', 
    'San Francisco Giants': 'SF', 'Houston Astros': 'HOU', 'Detroit Tigers': 'DET',
    'Texas Rangers': 'TEX', 'Toronto Blue Jays': 'TOR', 'Cincinnati Reds': 'CIN', 
    'Pittsburgh Pirates': 'PIT', 'Kansas City Royals': 'KC', 'Chicago White Sox': 'CWS',
    'Philadelphia Phillies': 'PHI', 'New York Mets': 'NYM', 'Arizona Diamondbacks': 'ARI', 
    'Tampa Bay Rays': 'TB', 'Colorado Rockies': 'COL', 'Minnesota Twins': 'MIN',
    'Boston Red Sox': 'BOS', 'New York Yankees': 'NYY', 'Baltimore Orioles': 'BAL', 
    'Washington Nationals': 'WSH', 'Milwaukee Brewers': 'MIL', 'Chicago Cubs': 'CHC',
    'Cleveland Guardians': 'CLE', 'Seattle Mariners': 'SEA', 'St. Louis Cardinals': 'STL', 
    'Miami Marlins': 'MIA', 'Los Angeles Angels': 'LAA', 'Oakland Athletics': 'OAK'
}

# --- 2. 함수 모음 ---
@st.cache_data
def load_csv_data(file_name):
    return pd.read_csv(os.path.join('/content/', file_name))

def get_market_data(api_key):
    url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
    params = {'apiKey': api_key, 'regions': 'us', 'markets': 'h2h', 'oddsFormat': 'decimal'}
    response = requests.get(url, params=params)
    return response.json()

# --- 3. 사이드바 및 메인 로직 ---
mode = st.sidebar.radio("분석 모드", ["배당 분석", "데이터 통계 분석", "공식 정보", "PyBaseball 분석"])

if mode == "배당 분석":
    st.header("📈 실시간 배당 분석")
    api_key = st.text_input("Odds API Key 입력", type="password")
    if st.button("분석 시작"):
        data = get_market_data(api_key)
        for match in data:
            home, away = match['home_team'], match['away_team']
            odds = match['bookmakers'][0]['markets'][0]['outcomes']
            h_odds = next(o['price'] for o in odds if o['name'] == home)
            st.write(f"**{away} vs {home}** | 배당: {h_odds}")

elif mode == "데이터 통계 분석":
    st.header("📊 로컬 CSV 파일 분석")
    files = [f for f in os.listdir('/content/') if f.endswith('.csv')]
    selected_file = st.selectbox("파일 선택", files)
    if selected_file:
        df = load_csv_data(selected_file)
        st.dataframe(df)

elif mode == "공식 정보":
    st.header("⚡ MLB 공식 API")
    team_name = st.text_input("팀 이름 입력")
    if st.button("조회"):
        st.json(statsapi.lookup_team(team_name))

elif mode == "PyBaseball 분석":
    st.header("⚾ PyBaseball 실시간 데이터")
    start_date = st.date_input("시작 날짜")
    end_date = st.date_input("종료 날짜")
    if st.button("데이터 불러오기"):
        data = statcast(start_dt=str(start_date), end_dt=str(end_date))
        st.dataframe(data)

st.divider()
st.caption("시스템 상태: 통합 완료 | 경로: /content/")
