import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

# 1. 팀 매칭 딕셔너리
NAME_MAP = {
    "Arizona D'Backs": "ARI", "Arizona Diamondbacks": "ARI", "Athletics": "OAK",
    "Atlanta Braves": "ATL", "Baltimore Orioles": "BAL", "Boston Red Sox": "BOS",
    "Chicago Cubs": "CHC", "Chicago White Sox": "CWS", "Cincinnati Reds": "CIN",
    "Cleveland Guardians": "CLE", "Colorado Rockies": "COL", "Detroit Tigers": "DET",
    "Houston Astros": "HOU", "Kansas City Royals": "KC", "Los Angeles Angels": "LAA",
    "Los Angeles Dodgers": "LAD", "Miami Marlins": "MIA", "Milwaukee Brewers": "MIL",
    "Minnesota Twins": "MIN", "New York Mets": "NYM", "New York Yankees": "NYY",
    "Oakland Athletics": "OAK", "Philadelphia Phillies": "PHI", "Pittsburgh Pirates": "PIT",
    "San Diego Padres": "SD", "San Francisco Giants": "SF", "Seattle Mariners": "SEA",
    "St. Louis Cardinals": "STL", "Tampa Bay Rays": "TB", "Texas Rangers": "TEX",
    "Toronto Blue Jays": "TOR", "Washington Nationals": "WSH"
}

def normalize_team_name(name):
    return NAME_MAP.get(name, name)

# 2. 모든 함수 정의 (오류 방지를 위해 상단 배치)
@st.cache_data
def get_mlb_schedule(target_date):
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={target_date}&hydrate=probablePitcher,linescore"
    try:
        response = requests.get(url, timeout=10).json()
        games = response['dates'][0]['games']
        kst = pytz.timezone('Asia/Seoul')
        data = []
        for g in games:
            utc_dt = datetime.strptime(g['gameDate'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
            kst_dt = utc_dt.astimezone(kst)
            ls = g.get('linescore', {})
            data.append({
                "경기시간(KST)": kst_dt.strftime('%H:%M'),
                "홈팀": normalize_team_name(g['teams']['home']['team']['name']),
                "원정팀": normalize_team_name(g['teams']['away']['team']['name']),
                "스코어": f"{ls.get('teams', {}).get('away', {}).get('runs', 0)} : {ls.get('teams', {}).get('home', {}).get('runs', 0)}",
                "홈선발": g['teams']['home'].get('probablePitcher', {}).get('fullName', '미정'),
                "원정선발": g['teams']['away'].get('probablePitcher', {}).get('fullName', '미정')
            })
        return data
    except: return []

@st.cache_data
def get_processed_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    df['h_team'] = df['home_team'].map(NAME_MAP)
    df['a_team'] = df['away_team'].map(NAME_MAP)
    return df

def calculate_win_prob(h_team, a_team, df):
    matchup = df[(df['h_team'] == h_team) & (df['a_team'] == a_team)]
    if matchup.empty: return 50.0
    h_avg = matchup['home_score'].mean()
    a_avg = matchup['away_score'].mean()
    if (h_avg + a_avg) == 0: return 50.0
    return round((h_avg / (h_avg + a_avg)) * 100, 1)

# 3. 사이드바 및 UI
st.set_page_config(layout="wide", page_title="MLB 통합 분석기")
menu = st.sidebar.radio("메뉴", ["경기 기록 및 일정 조회", "AI 승패 예측"])

if menu == "경기 기록 및 일정 조회":
    st.subheader("날짜별 MLB 상세 기록")
    date_val = st.date_input("날짜 선택:", datetime.now(), min_value=datetime(2024, 1, 1))
    if st.button("조회"):
        st.table(pd.DataFrame(get_mlb_schedule(date_val.strftime('%Y-%m-%d'))))

elif menu == "AI 승패 예측":
    st.subheader("데이터 기반 승률 예측")
    if st.button("예측 분석 실행"):
        master_df = get_processed_data()
        schedule = get_mlb_schedule(datetime.now().strftime('%Y-%m-%d'))
        results = [{"홈팀": g['홈팀'], "원정팀": g['원정팀'], "예상 승률": f"{calculate_win_prob(g['홈팀'], g['원정팀'], master_df)}%"} for g in schedule]
        st.table(pd.DataFrame(results))
