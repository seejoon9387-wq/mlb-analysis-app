import streamlit as st
import pandas as pd
import requests
import pytz
from datetime import datetime

# 1. 페이지 설정 및 팀 매칭 딕셔너리 (기존 유지)
st.set_page_config(layout="wide", page_title="MLB AI 엔진 v4.1")
TEAM_MAP = {
    "Baltimore Orioles": "BAL", "Boston Red Sox": "BOS", "New York Yankees": "NYY",
    "Toronto Blue Jays": "TOR", "Tampa Bay Rays": "TB", "Chicago White Sox": "CWS",
    "Cleveland Guardians": "CLE", "Detroit Tigers": "DET", "Kansas City Royals": "KC",
    "Minnesota Twins": "MIN", "Houston Astros": "HOU", "Los Angeles Angels": "LAA",
    "Oakland Athletics": "OAK", "Seattle Mariners": "SEA", "Texas Rangers": "TEX",
    "Atlanta Braves": "ATL", "Miami Marlins": "MIA", "New York Mets": "NYM",
    "Philadelphia Phillies": "PHI", "Washington Nationals": "WSH", "Chicago Cubs": "CHC",
    "Cincinnati Reds": "CIN", "Milwaukee Brewers": "MIL", "Pittsburgh Pirates": "PIT",
    "St. Louis Cardinals": "STL", "Arizona Diamondbacks": "ARI", "Colorado Rockies": "COL",
    "Los Angeles Dodgers": "LAD", "San Diego Padres": "SD", "San Francisco Giants": "SF"
}

# 2. 기능 함수 (v4.0 유지)
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
                "홈팀": TEAM_MAP.get(g['teams']['home']['team']['name'], g['teams']['home']['team']['name']),
                "원정팀": TEAM_MAP.get(g['teams']['away']['team']['name'], g['teams']['away']['team']['name'])
            })
        return data
    except: return []

@st.cache_data
def load_full_data():
    url_res = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    url_stats = 'https://drive.google.com/uc?export=download&id=1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH&confirm=t'
    try:
        df_res = pd.read_csv(url_res)
        # 모든 팀 리스트 추출 (home/away 모두 포함)
        all_teams_in_db = pd.concat([df_res['home_team'], df_res['away_team']]).unique()
        return sorted(list(all_teams_in_db))
    except: return None

# 3. 메뉴 및 전체 검증 로직
menu = st.sidebar.radio("메뉴", ["실시간 일정", "전체 팀 매칭 검증"])

if menu == "실시간 일정":
    st.subheader("오늘의 경기 일정")
    st.table(pd.DataFrame(get_mlb_schedule()))

elif menu == "전체 팀 매칭 검증":
    st.subheader("데이터베이스 전체 팀 목록 vs 실시간 팀")
    if st.button("전체 검증 시작"):
        db_teams = load_full_data()
        schedule = get_mlb_schedule()
        
        if db_teams:
            st.write(f"### DB에 존재하는 총 {len(db_teams)}개 팀")
            st.write(db_teams) # 전체 리스트 출력
            
            # 실시간 경기와 비교
            today_teams = set([g['홈팀'] for g in schedule] + [g['원정팀'] for g in schedule])
            missing = [t for t in today_teams if t not in db_teams]
            
            if not missing:
                st.success("✅ 오늘 경기 팀들이 모두 DB에 존재합니다!")
            else:
                st.warning(f"⚠️ 데이터셋에 없는 팀: {missing}")
