import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

# 1. 팀 이름 정규화 딕셔너리 (최대한 광범위하게 작성)
NAME_MAP = {
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

def normalize_team_name(name):
    # 매핑되지 않는 경우를 대비해 원본 로그를 남기거나 유연하게 처리
    return NAME_MAP.get(name, name)

@st.cache_data
def load_and_fix_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    
    # 1. 원본 데이터의 팀 리스트를 확인 (진단용)
    unique_db_teams = pd.concat([df['home_team'], df['away_team']]).unique()
    
    # 2. 팀 병합 및 정규화
    df_home = df[['home_team', 'home_score']].rename(columns={'home_team': 'team', 'home_score': 'score'})
    df_away = df[['away_team', 'away_score']].rename(columns={'away_team': 'team', 'away_score': 'score'})
    df_combined = pd.concat([df_home, df_away])
    df_combined['team'] = df_combined['team'].apply(lambda x: NAME_MAP.get(x, x))
    
    return df_combined, unique_db_teams

@st.cache_data
def get_mlb_schedule(target_date):
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={target_date}&hydrate=probablePitcher,linescore"
    try:
        response = requests.get(url, timeout=10).json()
        games = response['dates'][0]['games']
        data = []
        for g in games:
            home_name = g['teams']['home']['team']['name']
            away_name = g['teams']['away']['team']['name']
            data.append({
                "홈팀(원본)": home_name,
                "원정팀(원본)": away_name,
                "홈팀(매칭)": normalize_team_name(home_name),
                "원정팀(매칭)": normalize_team_name(away_name)
            })
        return data
    except: return []

# 3. 사이드바 및 진단 실행
st.sidebar.subheader("매칭 진단 모드")
if st.sidebar.button("매칭 전체 점검"):
    master_df, db_teams = load_and_fix_data()
    schedule = get_mlb_schedule(datetime.now().strftime('%Y-%m-%d'))
    
    st.subheader("진단 결과")
    st.write("### 데이터베이스 내 팀 이름 목록")
    st.write(db_teams)
    
    st.write("### 실시간 API 매칭 상태")
    st.table(pd.DataFrame(schedule))
    
    st.info("왼쪽 '매칭' 열이 우리가 사용하는 3글자 약어(BAL, NYY 등)로 잘 변환되었는지 확인하세요.")
