import streamlit as st
import requests

# 1. 설정
API_KEY = '9c3c5d2369ad9163a19c3e88dfa1f9c5'
TEAM_NAME_MAP = {
    'Dodgers': 'LAD', 'Padres': 'SD', 'Braves': 'ATL', 'Giants': 'SF',
    'Astros': 'HOU', 'Tigers': 'DET', 'Rangers': 'TEX', 'Blue Jays': 'TOR',
    'Reds': 'CIN', 'Pirates': 'PIT', 'Royals': 'KC', 'White Sox': 'CWS',
    'Phillies': 'PHI', 'Mets': 'NYM', 'Diamondbacks': 'ARI', 'Rays': 'TB',
    'Rockies': 'COL', 'Twins': 'MIN', 'Red Sox': 'BOS', 'Yankees': 'NYY',
    'Orioles': 'BAL', 'Nationals': 'WSH', 'Brewers': 'MIL', 'Cubs': 'CHC',
    'Guardians': 'CLE', 'Mariners': 'SEA', 'Cardinals': 'STL', 'Marlins': 'MIA',
    'Angels': 'LAA', 'Athletics': 'OAK'
}

# 2. 메인 화면
st.title("⚾ 직접 입력형 MLB 분석기")

# 입력창
home_team = st.text_input("홈 팀 이름을 입력하세요 (예: Yankees)", "")
away_team = st.text_input("원정 팀 이름을 입력하세요 (예: Red Sox)", "")

if st.button("분석 시작"):
    if not home_team or not away_team:
        st.warning("두 팀의 이름을 모두 입력해주세요!")
    else:
        st.info(f"분석 중: {away_team} vs {home_team}...")
        
        # API에서 전체 데이터 가져오기
        url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {'apiKey': API_KEY, 'regions': 'us', 'markets': 'h2h', 'oddsFormat': 'decimal'}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            found = False
            for match in data:
                # 사용자가 입력한 팀이 포함된 경기 찾기
                if (home_team.lower() in match['home_team'].lower()) and (away_team.lower() in match['away_team'].lower()):
                    st.success("✅ 경기 데이터를 찾았습니다!")
                    
                    # 배당률 정보
                    outcomes = match['bookmakers'][0]['markets'][0]['outcomes']
                    home_odds = next(o['price'] for o in outcomes if o['name'] == match['home_team'])
                    away_odds = next(o['price'] for o in outcomes if o['name'] == match['away_team'])
                    
                    # 결과 보여주기
                    st.write(f"### 📊 분석 결과")
                    st.metric(label=f"{match['home_team']} 승리 배당", value=home_odds)
                    st.metric(label=f"{match['away_team']} 승리 배당", value=away_odds)
                    found = True
                    break
            if not found:
                st.error("해당 매치업을 찾을 수 없습니다. 팀 이름을 정확히 입력했는지 확인해주세요.")
        else:
            st.error("데이터 서버 연결에 실패했습니다.")

# 기존 코드의 '분석 시작' 버튼 부분 아래에 추가하세요
import datetime

# 날짜 선택기 추가
selected_date = st.date_input("경기 날짜를 선택하세요", datetime.date.today())

if st.button("분석 시작"):
    # ... (기존 코드)
    # 데이터 매칭 부분에서 날짜 비교 추가
    for match in data:
        # API의 commence_time은 ISO 형식(예: 2026-06-28T... )입니다.
        match_date = match['commence_time'][:10] # 날짜만 잘라내기
        if (home_team.lower() in match['home_team'].lower()) and (str(selected_date) == match_date):
             # 여기서 분석 진행...
