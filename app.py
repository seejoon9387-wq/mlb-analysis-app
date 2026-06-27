import streamlit as st
import requests
import datetime

# 1. 설정
API_KEY = '9c3c5d2369ad9163a19c3e88dfa1f9c5'

# 2. 메인 화면
st.title("⚾ 날짜 선택형 MLB 분석기")

# 입력창들
selected_date = st.date_input("경기 날짜를 선택하세요", datetime.date.today())
home_team = st.text_input("홈 팀 이름 (예: Yankees)", "")
away_team = st.text_input("원정 팀 이름 (예: Red Sox)", "")

if st.button("분석 시작"):
    if not home_team or not away_team:
        st.warning("두 팀의 이름을 모두 입력해주세요!")
    else:
        st.info(f"{selected_date} 경기 분석 중: {away_team} vs {home_team}...")
        
        url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {'apiKey': API_KEY, 'regions': 'us', 'markets': 'h2h', 'oddsFormat': 'decimal'}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            found = False
            for match in data:
                # 날짜 및 팀 매칭 로직
                match_date = match['commence_time'][:10]
                if (str(selected_date) == match_date) and \
                   (home_team.lower() in match['home_team'].lower()) and \
                   (away_team.lower() in match['away_team'].lower()):
                    
                    st.success("✅ 경기 데이터를 찾았습니다!")
                    outcomes = match['bookmakers'][0]['markets'][0]['outcomes']
                    home_odds = next(o['price'] for o in outcomes if o['name'] == match['home_team'])
                    away_odds = next(o['price'] for o in outcomes if o['name'] == match['away_team'])
                    
                    st.write("### 📊 분석 결과")
                    st.metric(label=f"{match['home_team']} 승리 배당", value=home_odds)
                    st.metric(label=f"{match['away_team']} 승리 배당", value=away_odds)
                    found = True
                    break
            
            if not found:
                st.error("해당 날짜에 일치하는 경기 데이터를 찾을 수 없습니다.")
        else:
            st.error("데이터 서버 연결에 실패했습니다.")
