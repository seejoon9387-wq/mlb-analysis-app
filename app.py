import streamlit as st
import pandas as pd
import requests
import pytz
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="MLB AI 엔진 v5.0")

# 2. 팀 매칭 딕셔너리
NAME_MAP = {
    "Arizona D'Backs": "ARI", "Athletics": "OAK", "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL", "Boston Red Sox": "BOS", "Chicago Cubs": "CHC",
    "Chicago White Sox": "CWS", "Cincinnati Reds": "CIN", "Cleveland Guardians": "CLE",
    "Colorado Rockies": "COL", "Detroit Tigers": "DET", "Houston Astros": "HOU",
    "Kansas City Royals": "KC", "Los Angeles Angels": "LAA", "Los Angeles Dodgers": "LAD",
    "Miami Marlins": "MIA", "Milwaukee Brewers": "MIL", "Minnesota Twins": "MIN",
    "New York Mets": "NYM", "New York Yankees": "NYY", "Oakland Athletics": "OAK",
    "Philadelphia Phillies": "PHI", "Pittsburgh Pirates": "PIT", "San Diego Padres": "SD",
    "San Francisco Giants": "SF", "Seattle Mariners": "SEA", "St. Louis Cardinals": "STL",
    "Tampa Bay Rays": "TB", "Texas Rangers": "TEX", "Toronto Blue Jays": "TOR",
    "Washington Nationals": "WSH"
}

# 3. 모든 함수 정의 (오류 방지를 위해 맨 위로 이동)
def normalize_team_name(name):
    return NAME_MAP.get(name, name)

@st.cache_data
def get_mlb_schedule():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={today}&hydrate=probablePitcher"
    try:
        response = requests.get(url, timeout=10).json()
        games = response['dates'][0]['games']
        data = []
        for g in games:
            data.append({
                "홈팀": normalize_team_name(g['teams']['home']['team']['name']),
                "원정팀": normalize_team_name(g['teams']['away']['team']['name'])
            })
        return data
    except: return []

@st.cache_data
def load_fixed_data():
    url_res = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    try:
        df_res = pd.read_csv(url_res)
        return df_res
    except: return None

# 4. 사이드바 메뉴
menu = st.sidebar.radio("메뉴", ["실시간 일정", "AI 승패 예측"])

# 5. 메뉴별 실행 로직
if menu == "실시간 일정":
    st.subheader("오늘의 경기 일정")
    schedule = get_mlb_schedule()
    st.table(pd.DataFrame(schedule))

elif menu == "AI 승패 예측":
    st.subheader("오늘의 경기 승률 예측")
    if st.button("예측 시작"):
        schedule = get_mlb_schedule()
        if schedule:
            results = []
            for game in schedule:
                results.append({
                    "홈팀": game['홈팀'],
                    "원정팀": game['원정팀'],
                    "예상 승률": "데이터 분석 중..."
                })
            st.table(pd.DataFrame(results))
        else:
            st.warning("경기를 불러올 수 없습니다.")
