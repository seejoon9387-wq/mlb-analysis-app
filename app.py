import streamlit as st
import pandas as pd
import requests
import pytz
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="MLB AI 엔진 v4.0")

# 2. 팀 매칭 딕셔너리 (기존 기능)
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

# 3. 기능 함수들
@st.cache_data
def get_mlb_schedule():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={today}&hydrate=probablePitcher"
    try:
        response = requests.get(url, timeout=10).json()
        games = response['dates'][0]['games']
        kst = pytz.timezone('Asia/Seoul')
        data = []
        for g in games:
            utc_dt = datetime.strptime(g['gameDate'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
            data.append({
                "시간(KST)": utc_dt.astimezone(kst).strftime('%H:%M'),
                "홈팀": TEAM_MAP.get(g['teams']['home']['team']['name'], g['teams']['home']['team']['name']),
                "원정팀": TEAM_MAP.get(g['teams']['away']['team']['name'], g['teams']['away']['team']['name']),
                "홈선발": g['teams']['home'].get('probablePitcher', {}).get('fullName', '미정'),
                "원정선발": g['teams']['away'].get('probablePitcher', {}).get('fullName', '미정')
            })
        return data
    except: return []

@st.cache_data
def load_and_fix_data():
    # 보안 경고 우회 파라미터(&confirm=t) 추가된 통합 로드
    url_res = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    url_stats = 'https://drive.google.com/uc?export=download&id=1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH&confirm=t'
    try:
        df_res = pd.read_csv(url_res)
        df_home = df_res[['home_team', 'home_score']].rename(columns={'home_team': 'team', 'home_score': 'score'})
        df_away = df_res[['away_team', 'away_score']].rename(columns={'away_team': 'team', 'away_score': 'score'})
        return pd.concat([df_home, df_away])
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return None

# 4. 메뉴 구성
menu = st.sidebar.radio("메뉴", ["실시간 일정", "데이터 매칭 테스트"])

if menu == "실시간 일정":
    st.subheader("오늘의 경기 일정 및 선발 투수")
    st.table(pd.DataFrame(get_mlb_schedule()))

elif menu == "데이터 매칭 테스트":
    st.subheader("데이터 정합성 및 병합 테스트")
    if st.button("병합 시작"):
        master_df = load_and_fix_data()
        if master_df is not None:
            st.success("데이터 로드 및 병합 성공!")
            st.write(master_df.head())
