import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. 팀 매칭 딕셔너리 보완
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
def load_and_fix_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    # 데이터 진단용: 원본 컬럼 확인
    df_home = df[['home_team', 'home_score']].rename(columns={'home_team': 'team', 'home_score': 'score'})
    df_away = df[['away_team', 'away_score']].rename(columns={'away_team': 'team', 'away_score': 'score'})
    # team 이름 정규화 적용
    df_combined = pd.concat([df_home, df_away])
    df_combined['team'] = df_combined['team'].apply(normalize_team_name)
    return df_combined

def get_prediction(home, away, master_df):
    h_data = master_df[master_df['team'] == home]
    a_data = master_df[master_df['team'] == away]
    
    if h_data.empty or a_data.empty: return 50.0
    
    h_avg = h_data['score'].mean()
    a_avg = a_data['score'].mean()
    
    # 0으로 나누기 방지
    if (h_avg + a_avg) == 0: return 50.0
    
    return round((h_avg / (h_avg + a_avg)) * 100, 1)

# 3. 사이드바 및 실행 로직
st.set_page_config(layout="wide", page_title="MLB AI 예측 v5.4")
menu = st.sidebar.radio("메뉴", ["실시간 일정", "AI 승패 예측"])

if menu == "실시간 일정":
    st.subheader("오늘의 경기 일정")
    st.table(pd.DataFrame(get_mlb_schedule()))

elif menu == "AI 승패 예측":
    st.subheader("데이터 기반 승률 예측")
    if st.button("예측 분석 실행"):
        schedule = get_mlb_schedule()
        master_df = load_and_fix_data()
        
        st.write(f"데이터셋 총 행 수: {len(master_df)}")
        
        results = []
        for game in schedule:
            prob = get_prediction(game['홈팀'], game['원정팀'], master_df)
            results.append({"홈팀": game['홈팀'], "원정팀": game['원정팀'], "홈팀 승리 확률": f"{prob}%"})
        st.table(pd.DataFrame(results))
