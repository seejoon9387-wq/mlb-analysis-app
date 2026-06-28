import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import pytz

# 1. 팀 매칭 딕셔너리
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

# 2. 한국 시간 변환 및 API 데이터 조회
@st.cache_data
def get_mlb_schedule(target_date):
    # hydrate=linescore를 추가하여 점수 정보 포함
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={target_date}&hydrate=probablePitcher,linescore"
    try:
        response = requests.get(url, timeout=10).json()
        games = response['dates'][0]['games']
        kst = pytz.timezone('Asia/Seoul')
        data = []
        for g in games:
            # UTC 시간을 KST로 변환
            utc_dt = datetime.strptime(g['gameDate'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
            kst_dt = utc_dt.astimezone(kst)
            
            # 스코어 정보 추출 (경기가 시작되지 않았으면 0)
            linescore = g.get('linescore', {})
            home_score = linescore.get('teams', {}).get('home', {}).get('runs', 0)
            away_score = linescore.get('teams', {}).get('away', {}).get('runs', 0)
            
            data.append({
                "경기시간(KST)": kst_dt.strftime('%H:%M'),
                "홈팀": normalize_team_name(g['teams']['home']['team']['name']),
                "원정팀": normalize_team_name(g['teams']['away']['team']['name']),
                "스코어": f"{away_score} : {home_score}",
                "홈선발": g['teams']['home'].get('probablePitcher', {}).get('fullName', '미정'),
                "원정선발": g['teams']['away'].get('probablePitcher', {}).get('fullName', '미정')
            })
        return data
    except: return []

# 3. 화면 구성
st.set_page_config(layout="wide", page_title="MLB 경기 기록 상세")
menu = st.sidebar.radio("메뉴", ["경기 기록 및 일정 조회", "AI 승패 예측"])

if menu == "경기 기록 및 일정 조회":
    st.subheader("날짜별 MLB 상세 경기 기록")
    selected_date = st.date_input("날짜 선택:", datetime.now(), min_value=datetime(2024, 1, 1))
    
    if st.button("조회"):
        schedule = get_mlb_schedule(selected_date.strftime('%Y-%m-%d'))
        if schedule:
            st.table(pd.DataFrame(schedule))
        else:
            st.warning("해당 날짜에 경기가 없거나 데이터를 불러올 수 없습니다.")
