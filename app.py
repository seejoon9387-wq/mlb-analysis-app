import streamlit as st
import requests

# 1. 설정 (API_KEY는 환경 변수로 관리하는 게 안전하지만, 지금은 여기에 넣습니다)
API_KEY = '9c3c5d2369ad9163a19c3e88dfa1f9c5' 
TEAM_NAME_MAP = {'Los Angeles Dodgers': 'LAD', 'San Diego Padres': 'SD', ...} # 위에서 주신 딕셔너리 그대로 복사
TEAM_METRICS = {'LAD': 1600, 'SD': 1550, ...} # 위에서 주신 딕셔너리 그대로 복사

# 2. 핵심 함수들 (가져오기)
def get_clean_market_data():
    url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
    params = {'apiKey': API_KEY, 'regions': 'us', 'markets': 'h2h', 'oddsFormat': 'decimal'}
    response = requests.get(url, params=params)
    return response.json()

def simulate_matchup(h_key, a_key):
    h_rating = TEAM_METRICS.get(h_key, 1500)
    a_rating = TEAM_METRICS.get(a_key, 1500)
    return 1 / (1 + 10 ** ((a_rating - h_rating) / 400))

# 3. 웹 화면 (Streamlit)
st.title("⚾ MLB 승부 예측 분석기")

if st.button("실시간 데이터 분석"):
    data = get_clean_market_data()
    results = []
    for match in data:
        home, away = match['home_team'], match['away_team']
        # 모델링 및 계산 로직 추가...
        prob_home = simulate_matchup(TEAM_NAME_MAP.get(home, home), TEAM_NAME_MAP.get(away, away))
        results.append({"홈팀": home, "원정팀": away, "모델 승률": f"{prob_home:.2%}"})
    
    st.table(results)
