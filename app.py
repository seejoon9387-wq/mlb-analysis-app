import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

# 1. 팀 매칭 딕셔너리 및 이름 정규화 (이전 버전과 동일)
NAME_MAP = {
    "Arizona D'Backs": "ARI", "Athletics": "OAK", "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL", "Boston Red Sox": "BOS", "Chicago Cubs": "CHC",
    "Chicago White Sox": "CWS", "Cincinnati Reds": "CIN", "Cleveland Guardians": "CLE",
    "Colorado Rockies": "COL", "Detroit Tigers": "DET", "Houston Astros": "HOU",
    "Kansas City Royals": "KC", "Los Angeles Angels": "LAA", "Los Angeles Dodgers": "LAD",
    "Miami Marlins": "MIA", "Milwaukee Brewers": "MIL", "Minnesota Twins": "MIN",
    "New York Mets": "NYM", "New York Yankees": "NYY", "Philadelphia Phillies": "PHI",
    "Pittsburgh Pirates": "PIT", "San Diego Padres": "SD", "San Francisco Giants": "SF",
    "Seattle Mariners": "SEA", "St. Louis Cardinals": "STL", "Tampa Bay Rays": "TB",
    "Texas Rangers": "TEX", "Toronto Blue Jays": "TOR", "Washington Nationals": "WSH"
}

def normalize_team_name(name):
    return NAME_MAP.get(name, name)

# 2. API 데이터 조회 함수 (날짜 매개변수 추가)
@st.cache_data
def get_mlb_schedule(target_date):
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={target_date}&hydrate=probablePitcher"
    try:
        response = requests.get(url, timeout=10).json()
        games = response['dates'][0]['games']
        data = []
        for g in games:
            data.append({
                "홈팀": normalize_team_name(g['teams']['home']['team']['name']),
                "원정팀": normalize_team_name(g['teams']['away']['team']['name']),
                "홈선발": g['teams']['home'].get('probablePitcher', {}).get('fullName', '미정'),
                "원정선발": g['teams']['away'].get('probablePitcher', {}).get('fullName', '미정')
            })
        return data
    except: return []

# 3. 사이드바 및 실행 로직
st.set_page_config(layout="wide", page_title="MLB 기록 조회 엔진")
menu = st.sidebar.radio("메뉴", ["경기 기록 및 일정 조회", "AI 승패 예측"])

if menu == "경기 기록 및 일정 조회":
    st.subheader("날짜별 MLB 경기 기록 및 일정")
    
    # 달력 생성 (2024-01-01부터 오늘까지)
    selected_date = st.date_input(
        "날짜를 선택하세요:", 
        datetime.now(),
        min_value=datetime(2024, 1, 1),
        max_value=datetime.now()
    )
    
    if st.button("조회"):
        date_str = selected_date.strftime('%Y-%m-%d')
        schedule = get_mlb_schedule(date_str)
        
        if schedule:
            st.success(f"{date_str} 경기 정보")
            st.table(pd.DataFrame(schedule))
        else:
            st.warning("해당 날짜에 예정된 경기가 없거나 데이터를 가져올 수 없습니다.")

elif menu == "AI 승패 예측":
    # (v5.4의 승패 예측 로직 유지)
    st.write("AI 승패 예측 로직입니다.")
