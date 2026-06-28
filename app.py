import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

# 1. 팀 매핑
NAME_MAP = {
    "Baltimore Orioles": "BAL", "Washington Nationals": "WSH", "Pittsburgh Pirates": "PIT",
    "Cincinnati Reds": "CIN", "Toronto Blue Jays": "TOR", "Texas Rangers": "TEX",
    "Detroit Tigers": "DET", "Houston Astros": "HOU", "Cleveland Guardians": "CLE",
    "Seattle Mariners": "SEA", "Tampa Bay Rays": "TB", "Arizona Diamondbacks": "ARI",
    "New York Mets": "NYM", "Philadelphia Phillies": "PHI", "Minnesota Twins": "MIN",
    "Colorado Rockies": "COL", "Chicago White Sox": "CWS", "Kansas City Royals": "KC",
    "Milwaukee Brewers": "MIL", "Chicago Cubs": "CHC", "St. Louis Cardinals": "STL",
    "Miami Marlins": "MIA", "Los Angeles Angels": "LAA", "Oakland Athletics": "OAK",
    "San Francisco Giants": "SF", "Atlanta Braves": "ATL", "San Diego Padres": "SD",
    "Los Angeles Dodgers": "LAD", "Boston Red Sox": "BOS", "New York Yankees": "NYY"
}

# 2. 데이터 가져오기 함수 (기능별 공통 사용)
@st.cache_data
def get_mlb_data(target_date):
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={target_date}&hydrate=linescore,probablePitcher"
    try:
        response = requests.get(url, timeout=10).json()
        games = response.get('dates', [{}])[0].get('games', [])
        data = []
        for g in games:
            ls = g.get('linescore', {})
            data.append({
                "경기시간": g['gameDate'].split('T')[1][:5],
                "홈팀": NAME_MAP.get(g['teams']['home']['team']['name'], g['teams']['home']['team']['name']),
                "원정팀": NAME_MAP.get(g['teams']['away']['team']['name'], g['teams']['away']['team']['name']),
                "홈득점": ls.get('teams', {}).get('home', {}).get('runs', 0),
                "원정득점": ls.get('teams', {}).get('away', {}).get('runs', 0),
                "상태": g['status']['detailedState']
            })
        return data
    except: return []

# 3. 사이드바 메뉴 구성
st.sidebar.title("MLB 분석 도구")
menu = st.sidebar.radio("메뉴 선택", ["경기 기록 및 일정 조회", "AI 승패 예측"])

# 4. 기능 실행 로직
if menu == "경기 기록 및 일정 조회":
    st.subheader("날짜별 MLB 경기 기록")
    selected_date = st.date_input("날짜 선택:", datetime.now())
    if st.button("조회"):
        data = get_mlb_data(selected_date.strftime('%Y-%m-%d'))
        if data:
            st.table(pd.DataFrame(data))
        else:
            st.write("해당 날짜의 경기 정보가 없습니다.")

elif menu == "AI 승패 예측":
    st.subheader("데이터 기반 승패 예측")
    if st.button("오늘 경기 예측 실행"):
        data = get_mlb_data(datetime.now().strftime('%Y-%m-%d'))
        if data:
            # 여기서는 단순히 오늘 데이터를 보여주되, 추후 승률 알고리즘 추가 가능
            st.table(pd.DataFrame(data))
        else:
            st.write("예측할 데이터가 없습니다.")
