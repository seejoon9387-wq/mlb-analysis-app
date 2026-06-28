import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

# 1. 완벽한 이름 매핑 (공식 명칭 업데이트)
NAME_MAP = {
    "Arizona Diamondbacks": "ARI", "Atlanta Braves": "ATL", "Baltimore Orioles": "BAL",
    "Boston Red Sox": "BOS", "Chicago Cubs": "CHC", "Chicago White Sox": "CWS",
    "Cincinnati Reds": "CIN", "Cleveland Guardians": "CLE", "Colorado Rockies": "COL",
    "Detroit Tigers": "DET", "Houston Astros": "HOU", "Kansas City Royals": "KC",
    "Los Angeles Angels": "LAA", "Los Angeles Dodgers": "LAD", "Miami Marlins": "MIA",
    "Milwaukee Brewers": "MIL", "Minnesota Twins": "MIN", "New York Mets": "NYM",
    "New York Yankees": "NYY", "Oakland Athletics": "OAK", "Philadelphia Phillies": "PHI",
    "Pittsburgh Pirates": "PIT", "San Diego Padres": "SD", "San Francisco Giants": "SF",
    "Seattle Mariners": "SEA", "St. Louis Cardinals": "STL", "Tampa Bay Rays": "TB",
    "Texas Rangers": "TEX", "Toronto Blue Jays": "TOR", "Washington Nationals": "WSH"
}

def get_match_key(team_name):
    # 공백 제거 및 대소문자 통일 후 매핑
    clean_name = team_name.strip()
    return NAME_MAP.get(clean_name, clean_name)

@st.cache_data
def get_mlb_schedule(target_date):
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={target_date}&hydrate=probablePitcher,linescore"
    try:
        response = requests.get(url, timeout=10).json()
        games = response['dates'][0]['games']
        data = []
        for g in games:
            # 원본 팀명
            home_raw = g['teams']['home']['team']['name']
            away_raw = g['teams']['away']['team']['name']
            
            # 매칭 시도
            home_match = get_match_key(home_raw)
            away_match = get_match_key(away_raw)
            
            ls = g.get('linescore', {})
            data.append({
                "홈팀(매칭)": home_match,
                "원정팀(매칭)": away_match,
                "홈팀(원본)": home_raw,
                "원정팀(원본)": away_raw,
                "스코어": f"{ls.get('teams', {}).get('away', {}).get('runs', 0)}:{ls.get('teams', {}).get('home', {}).get('runs', 0)}"
            })
        return data
    except: return []

# 2. UI 및 로직
st.set_page_config(layout="wide")
menu = st.sidebar.radio("메뉴", ["데이터 점검", "AI 예측"])

if menu == "데이터 점검":
    st.subheader("100% 매칭을 위한 팀 이름 진단")
    date_val = st.date_input("날짜 선택:", datetime.now())
    if st.button("진단 시작"):
        schedule = get_mlb_schedule(date_val.strftime('%Y-%m-%d'))
        df = pd.DataFrame(schedule)
        st.table(df)
        st.info("위 표에서 '홈팀(매칭)'이 3글자 약어로 나오지 않는다면, 그 이름을 알려주세요. 즉시 NAME_MAP에 추가하겠습니다.")

elif menu == "AI 예측":
    st.write("진단 완료 후 예측을 실행하세요.")
