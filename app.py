import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime
import pytz

# 1. 페이지 설정
st.set_page_config(layout="wide", page_title="MLB AI 엔진 v3.9.2")

# 2. 팀 매칭 딕셔너리
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

# 3. 함수 정의
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
                "원정팀": TEAM_MAP.get(g['teams']['away']['team']['name'], g['teams']['away']['team']['name']),
                "홈선발": g['teams']['home'].get('probablePitcher', {}).get('fullName', '미정'),
                "원정선발": g['teams']['away'].get('probablePitcher', {}).get('fullName', '미정')
            })
        return data
    except: return []

@st.cache_data
def fetch_master_data():
    try:
        # direct download 링크로 수정
        df_res = pd.read_csv('https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY')
        df_stats = pd.read_csv('https://drive.google.com/uc?export=download&id=1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH')
        return pd.merge(df_res, df_stats, on=['date', 'team'], how='inner')
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return None

# 4. 메뉴 구성
menu = st.sidebar.radio("메뉴", ["실시간 일정", "데이터 매칭 테스트"])

# 5. 실행 로직
if menu == "실시간 일정":
    st.subheader("오늘의 MLB 경기 일정")
    schedule = get_mlb_schedule()
    if schedule:
        st.table(pd.DataFrame(schedule))
    else:
        st.write("데이터를 가져올 수 없거나 오늘 경기가 없습니다.")

elif menu == "데이터 매칭 테스트":
    st.subheader("데이터셋 정합성 확인")
    if st.button("매칭 테스트 시작"):
        master_df = fetch_master_data()
        schedule = get_mlb_schedule()
        
        if master_df is not None and len(schedule) > 0:
            all_teams = set([g['홈팀'] for g in schedule] + [g['원정팀'] for g in schedule])
            csv_teams = set(master_df['team'].unique())
            missing = all_teams - csv_teams
            
            if not missing:
                st.success("✅ 모든 팀이 데이터셋에 존재합니다! 예측 모델 연동 준비 완료.")
            else:
                st.warning(f"⚠️ 매칭되지 않은 팀: {missing}")
                st.info("CSV 파일에 해당 팀들의 데이터가 포함되어 있는지 확인하세요.")
        else:
            st.error("데이터가 비어있습니다. 구글 드라이브 파일 공유 설정을 다시 확인해 주세요.")
