import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. 팀 매핑 딕셔너리 (가장 정확한 버전)
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

# 2. 데이터 처리 및 승률 계산 로직
@st.cache_data
def get_processed_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    # 팀 이름 통일
    df['h_team'] = df['home_team'].map(NAME_MAP)
    df['a_team'] = df['away_team'].map(NAME_MAP)
    return df

def calculate_win_prob(h_team, a_team, df):
    # 해당 두 팀이 붙었던 과거 기록만 필터링
    matchup = df[(df['h_team'] == h_team) & (df['a_team'] == a_team)]
    if matchup.empty:
        # 기록이 없으면 반대로도 검색
        matchup = df[(df['h_team'] == a_team) & (df['a_team'] == h_team)]
        if matchup.empty: return 50.0 # 진짜 기록 없으면 50%
        # 반대 기록이면 승률 반전
        avg_score = matchup['home_score'].mean() # 원래 원정팀의 홈 기록
        return round(100 - (avg_score / (avg_score + matchup['away_score'].mean()) * 100), 1)
    
    # 홈팀 승률 계산
    h_avg = matchup['home_score'].mean()
    a_avg = matchup['away_score'].mean()
    if (h_avg + a_avg) == 0: return 50.0
    return round((h_avg / (h_avg + a_avg)) * 100, 1)

# 3. 메인 화면
st.title("⚾ MLB AI 정밀 분석기")
if st.button("경기 데이터 매칭 및 분석 실행"):
    master_df = get_processed_data()
    schedule = get_mlb_schedule(datetime.now().strftime('%Y-%m-%d')) # 기존 함수 사용
    
    results = []
    for game in schedule:
        h = game['홈팀']
        a = game['원정팀']
        prob = calculate_win_prob(h, a, master_df)
        results.append({"홈팀": h, "원정팀": a, "예상 승률": f"{prob}%"})
    st.table(pd.DataFrame(results))
