# 버전: v3.6
# 패치 내용: NameError 해결 및 데이터 매칭 테스트 모드 추가
import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime
import pytz

# 1. 페이지 설정 (가장 상단에 배치)
st.set_page_config(layout="wide", page_title="MLB AI 엔진 v3.6")

# 2. 사이드바 메뉴 생성 (반드시 if문보다 위에 있어야 합니다)
menu = st.sidebar.radio("메뉴", ["실시간 일정", "학습 데이터셋 관리", "데이터 매칭 테스트"])

# 3. 매칭 및 API 함수 정의
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
        data = []
        for g in games:
            data.append({
                "홈팀": TEAM_MAP.get(g['teams']['home']['team']['name'], g['teams']['home']['team']['name']),
                "원정팀": TEAM_MAP.get(g['teams']['away']['team']['name'], g['teams']['away']['team']['name'])
            })
        return data
    except: return None

# 4. 메뉴별 화면 로직
if menu == "실시간 일정":
    st.subheader("오늘의 MLB 경기")
    st.table(pd.DataFrame(get_mlb_schedule()))

elif menu == "학습 데이터셋 관리":
    st.subheader("클라우드 데이터 병합 센터")
    if st.button("데이터 병합 실행"):
        st.write("병합 로직 실행 중...")

elif menu == "데이터 매칭 테스트":
    st.subheader("실시간 vs CSV 팀명 매칭 테스트")
    if st.button("테스트 시작"):
        api_df = pd.DataFrame(get_mlb_schedule())
        csv_df = load_drive_csv("1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY")
        
        api_teams = set(api_df['홈팀'].unique()) | set(api_df['원정팀'].unique())
        csv_teams = set(csv_df['team'].unique())
        
        missing = api_teams - csv_teams
        if not missing:
            st.success("✅ 모든 팀 데이터 매칭 완료!")
        else:
            st.warning(f"⚠️ 매칭되지 않은 팀: {missing}")
