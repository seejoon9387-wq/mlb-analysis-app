import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

# 1. 완벽한 팀 매핑 (약어 통일)
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

@st.cache_data
def get_live_mlb_data(target_date):
    # API 요청: 상세 점수와 진행 상태를 포함
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={target_date}&hydrate=linescore,game(content(summary))"
    response = requests.get(url).json()
    
    data = []
    if 'dates' in response and len(response['dates']) > 0:
        games = response['dates'][0]['games']
        for g in games:
            # 상태값(진행중/종료/예정) 확인
            status = g['status']['detailedState']
            home_name = g['teams']['home']['team']['name']
            away_name = g['teams']['away']['team']['name']
            
            # 스코어 처리
            ls = g.get('linescore', {})
            h_score = ls.get('teams', {}).get('home', {}).get('runs', 0) if status != 'Scheduled' else "-"
            a_score = ls.get('teams', {}).get('away', {}).get('runs', 0) if status != 'Scheduled' else "-"
            
            data.append({
                "홈팀": NAME_MAP.get(home_name, home_name),
                "원정팀": NAME_MAP.get(away_name, away_name),
                "상태": status,
                "스코어": f"{a_score} : {h_score}"
            })
    return data

# 2. 메인 UI
st.title("⚾ MLB 실시간 경기 데이터 (2026-06-29)")
if st.button("오늘 경기 정보 새로고침"):
    today_str = datetime.now(pytz.timezone('Asia/Seoul')).strftime('%Y-%m-%d')
    schedule = get_live_mlb_data(today_str)
    
    if schedule:
        st.table(pd.DataFrame(schedule))
    else:
        st.write("오늘 예정된 경기가 없거나 API에서 데이터를 불러오지 못했습니다.")
