import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

# 1. 설정 및 팀 매핑
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
def get_master_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    return pd.read_csv(url)

@st.cache_data
def get_mlb_schedule(date_str):
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={date_str}&hydrate=linescore"
    try:
        res = requests.get(url, timeout=10).json()
        games = res['dates'][0]['games']
        data = []
        for g in games:
            ls = g.get('linescore', {})
            data.append({
                "홈팀": NAME_MAP.get(g['teams']['home']['team']['name'], g['teams']['home']['team']['name']),
                "원정팀": NAME_MAP.get(g['teams']['away']['team']['name'], g['teams']['away']['team']['name']),
                "홈득점": ls.get('teams', {}).get('home', {}).get('runs', 0),
                "원정득점": ls.get('teams', {}).get('away', {}).get('runs', 0),
                "상태": g['status']['detailedState']
            })
        return pd.DataFrame(data)
    except: return pd.DataFrame()

# 2. UI 레이아웃
st.set_page_config(layout="wide", page_title="MLB 통합 엔진")
st.sidebar.title("통합 분석 메뉴")
menu = st.sidebar.radio("작업 선택", ["실시간 경기/달력 조회", "상대 전적 AI 예측"])

# 3. 메뉴별 기능
if menu == "실시간 경기/달력 조회":
    st.subheader("📅 날짜 선택 경기 기록")
    target_date = st.date_input("날짜를 선택하세요:", datetime.now())
    if st.button("조회"):
        df = get_mlb_schedule(target_date.strftime('%Y-%m-%d'))
        if not df.empty: st.table(df)
        else: st.warning("데이터가 없습니다.")

elif menu == "상대 전적 AI 예측":
    st.subheader("📊 CSV 기반 상대 전적 분석")
    if st.button("분석 실행"):
        master_df = get_master_data()
        live_df = get_mlb_schedule(datetime.now().strftime('%Y-%m-%d'))
        
        if not live_df.empty:
            results = []
            for _, row in live_df.iterrows():
                match = master_df[(master_df['home_team'] == row['홈팀']) & (master_df['away_team'] == row['원정팀'])]
                avg_h = match['home_score'].mean() if not match.empty else 0
                results.append({"홈팀": row['홈팀'], "원정팀": row['원정팀'], "평균 득점": round(avg_h, 1)})
            st.table(pd.DataFrame(results))
        else:
            st.write("오늘 경기가 없습니다.")
