import streamlit as st
import requests

# 1. 설정
API_KEY = '9c3c5d2369ad9163a19c3e88dfa1f9c5'

TEAM_NAME_MAP = {
    'Los Angeles Dodgers': 'LAD', 'San Diego Padres': 'SD',
    'Atlanta Braves': 'ATL', 'San Francisco Giants': 'SF',
    'Houston Astros': 'HOU', 'Detroit Tigers': 'DET',
    'Texas Rangers': 'TEX', 'Toronto Blue Jays': 'TOR',
    'Cincinnati Reds': 'CIN', 'Pittsburgh Pirates': 'PIT',
    'Kansas City Royals': 'KC', 'Chicago White Sox': 'CWS',
    'Philadelphia Phillies': 'PHI', 'New York Mets': 'NYM',
    'Arizona Diamondbacks': 'ARI', 'Tampa Bay Rays': 'TB',
    'Colorado Rockies': 'COL', 'Minnesota Twins': 'MIN',
    'Boston Red Sox': 'BOS', 'New York Yankees': 'NYY',
    'Baltimore Orioles': 'BAL', 'Washington Nationals': 'WSH',
    'Milwaukee Brewers': 'MIL', 'Chicago Cubs': 'CHC',
    'Cleveland Guardians': 'CLE', 'Seattle Mariners': 'SEA',
    'St. Louis Cardinals': 'STL', 'Miami Marlins': 'MIA',
    'Los Angeles Angels': 'LAA', 'Oakland Athletics': 'OAK',
    'Angels': 'LAA', 'Athletics': 'OAK'
}

TEAM_METRICS = {
    'LAD': 1600, 'SD': 1550, 'NYY': 1650, 'BOS': 1500, 'HOU': 1580,
    'DET': 1480, 'ATL': 1620, 'SF': 1520, 'TEX': 1530, 'TOR': 1510,
    'CIN': 1490, 'PIT': 1470, 'KC': 1520, 'CWS': 1400, 'PHI': 1610,
    'NYM': 1540, 'ARI': 1530, 'TB': 1550, 'COL': 1420, 'MIN': 1560,
    'BAL': 1630, 'WSH': 1450, 'MIL': 1570, 'CHC': 1500, 'CLE': 1580,
    'SEA': 1540, 'STL': 1510, 'MIA': 1430, 'LAA': 1460, 'OAK': 1380
}

# 2. 핵심 함수들
def get_clean_market_data():
    url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
    params = {'apiKey': API_KEY, 'regions': 'us', 'markets': 'h2h', 'oddsFormat': 'decimal'}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else []

def simulate_matchup(h_key, a_key):
    h_rating = TEAM_METRICS.get(h_key, 1500)
    a_rating = TEAM_METRICS.get(a_key, 1500)
    return 1 / (1 + 10 ** ((a_rating - h_rating) / 400))

# 3. 웹 화면 (Streamlit)
st.title("⚾ MLB 승부 예측 분석기")

if st.button("실시간 데이터 분석"):
    with st.spinner('API에서 데이터를 가져오는 중...'):
        data = get_clean_market_data()
        if not data:
            st.error("데이터를 불러올 수 없습니다. API 키를 확인하세요.")
        else:
            results = []
            for match in data:
                home, away = match['home_team'], match['away_team']
                h_key = TEAM_NAME_MAP.get(home, home)
                a_key = TEAM_NAME_MAP.get(away, away)
                prob_home = simulate_matchup(h_key, a_key)
                results.append({"홈팀": home, "원정팀": away, "모델 승률": f"{prob_home:.2%}"})
            
            st.table(results)
