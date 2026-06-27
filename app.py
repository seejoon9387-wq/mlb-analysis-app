import streamlit as st
import requests
import pandas as pd
import datetime
import pytz

# 1. 설정
API_KEY = '9c3c5d2369ad9163a19c3e88dfa1f9c5'

# 2. 메인 화면
st.title("⚾ MLB 통합 분석기")

# 입력창들
selected_date = st.date_input("경기 날짜를 선택하세요", datetime.date.today())
home_team = st.text_input("홈 팀 이름 (예: Yankees)", "")
away_team = st.text_input("원정 팀 이름 (예: Red Sox)", "")

if st.button("분석 시작"):
    if not home_team or not away_team:
        st.warning("두 팀의 이름을 모두 입력해주세요!")
    else:
        st.info(f"{selected_date} 경기 분석 중...")
        
        # API에서 데이터 가져오기
        url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {'apiKey': API_KEY, 'regions': 'us', 'markets': 'h2h', 'oddsFormat': 'decimal'}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            found = False
            kst = pytz.timezone('Asia/Seoul')
            
            for match in data:
                # 시간대 변환 로직
                match_dt_utc = datetime.datetime.fromisoformat(match['commence_time'].replace('Z', '+00:00'))
                match_dt_kst = match_dt_utc.astimezone(kst)
                
                # 팀 이름 필터링 (사용자 입력 포함 여부)
                if (selected_date == match_dt_kst.date()) and \
                   (home_team.lower() in match['home_team'].lower()) and \
                   (away_team.lower() in match['away_team'].lower()):
                    
                    st.success("✅ 경기 데이터를 찾았습니다!")
                    
                    # 배당률 추출
                    outcomes = match['bookmakers'][0]['markets'][0]['outcomes']
                    h_odds = next(o['price'] for o in outcomes if o['name'] == match['home_team'])
                    a_odds = next(o['price'] for o in outcomes if o['name'] == match['away_team'])
                    
                    st.write("### 📊 분석 결과")
                    st.metric(label=f"홈팀: {match['home_team']} 배당", value=h_odds)
                    st.metric(label=f"원정팀: {match['away_team']} 배당", value=a_odds)
                    found = True
                    break
            
            if not found:
                st.error("해당 날짜와 팀에 맞는 경기 데이터를 찾을 수 없습니다.")
        else:
            st.error("API 서버 연결에 실패했습니다.")
