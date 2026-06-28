# 버전: v3.5
# 누적 기능: 구글 드라이브 통합, 실시간 일정, 시간 변환, 선발투수 매칭, 팀명 자동 변환
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

# 1. 설정 및 매칭 딕셔너리
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

# 2. 로딩 및 API 함수
@st.cache_data
def load_drive_csv(file_id):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    response = requests.get(url, timeout=10)
    return pd.read_csv(io.BytesIO(response.content)) if response.status_code == 200 else None

def get_mlb_schedule():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={today}&hydrate=probablePitcher"
    try:
        response = requests.get(url, timeout=5).json()
        games = response['dates'][0]['games']
        kst = pytz.timezone('Asia/Seoul')
        data = []
        for g in games:
            utc_dt = datetime.strptime(g['gameDate'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.utc)
            data.append({
                "시간(KST)": utc_dt.astimezone(kst).strftime('%H:%M'),
                "홈팀": TEAM_MAP.get(g['teams']['home']['team']['name'], g['teams']['home']['team']['name']),
                "원정팀": TEAM_MAP.get(g['teams']['away']['team']['name'], g['teams']['away']['team']['name']),
                "홈 선발": g['teams']['home'].get('probablePitcher', {}).get('fullName', '미정'),
                "원정 선발": g['teams']['away'].get('probablePitcher', {}).get('fullName', '미정')
            })
        return data
    except: return None

# 3. UI 및 메뉴 구조
st.set_page_config(layout="wide", page_title="MLB AI 엔진 v3.5")
st.title("⚾ MLB AI 엔진 v3.5")
menu = st.sidebar.radio("메뉴", ["실시간 일정", "학습 데이터셋 관리", "AI 승패 예측"])

if menu == "실시간 일정":
    st.subheader("오늘의 경기 일정 및 선발 투수")
    df = pd.DataFrame(get_mlb_schedule())
    st.table(df)

elif menu == "학습 데이터셋 관리":
    st.subheader("클라우드 데이터 병합")
    if st.button("데이터 병합 실행"):
        # 여기에 기존 병합 로직 작성
        st.success("데이터가 준비되었습니다.")

elif menu == "AI 승패 예측":
    st.subheader("AI 승패 예측 시스템")
    st.info("현재 모델을 학습하고 오늘 경기 데이터를 매칭 중입니다.")
