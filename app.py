import streamlit as st
import requests
import datetime
import pytz

# 1. 설정
API_KEY = '9c3c5d2369ad9163a19c3e88dfa1f9c5'

# 2. 메인 화면
st.title("⚾ MLB 승부 예측 분석기")

# 입력창들 (날짜 및 팀 입력)
selected_date = st.date_input("경기 날짜를 선택하세요", datetime.date.today())
home_team = st.text_input("홈 팀 이름 (예: Yankees)", "")
away_team = st.text_input("원정 팀 이름 (예: Red Sox)", "")

if st.button("분석 실행"):
    if not home_team or not away_team:
        st.warning("두 팀의 이름을 모두 입력해주세요!")
    else:
        st.info(f"{selected_date} 경기 데이터를 불러오는 중...")
        
        # API에서 데이터 가져오기
        url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"
        params = {'apiKey': API_KEY, 'regions': 'us', 'markets': 'h2h', 'oddsFormat': 'decimal'}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            found = False
            kst = pytz.timezone('Asia/Seoul')
            
            for match in data:
                # 시간대 변환 로직 (미국 시간 -> 한국 시간)
                match_dt_utc = datetime.datetime.fromisoformat(match['commence_time'].replace('Z', '+00:00'))
                match_dt_kst = match_dt_utc.astimezone(kst)
                
                # 날짜 및 팀 필터링
                if (selected_date == match_dt_kst.date()) and \
                   (home_team.lower() in match['home_team'].lower()) and \
                   (away_team.lower() in match['away_team'].lower()):
                    
                    st.success("✅ 경기 데이터를 찾았습니다!")
                    
                    # 배당률 정보
                    outcomes = match['bookmakers'][0]['markets'][0]['outcomes']
                    h_odds = next(o['price'] for o in outcomes if o['name'] == match['home_team'])
                    a_odds = next(o['price'] for o in outcomes if o['name'] == match['away_team'])
                    
                    st.write("### 📊 분석 결과")
                    st.metric(label=f"홈팀: {match['home_team']} 승리 배당", value=h_odds)
                    st.metric(label=f"원정팀: {match['away_team']} 승리 배당", value=a_odds)
                    found = True
                    break
            
            if not found:
                st.error("해당 날짜에 일치하는 경기를 찾을 수 없습니다. 팀 이름을 다시 확인해 보세요.")
        else:
            st.error("데이터 서버 연결에 실패했습니다.")


# --- [추가] 리그 평균 지표 리포트 탭 ---
# 탭 구조를 만들었다면 그 아래에 이 기능을 넣어보세요
def get_team_power_metrics(df):
    # 필요한 컬럼이 있는지 확인 후 계산
    required_cols = ['avg_hit_speed', 'brl_percent', 'barrels']
    if all(col in df.columns for col in required_cols):
        power_summary = df.groupby(['Year', 'Metric'])[required_cols].mean()
        return power_summary
    return None

# 리포트 출력 예시 (웹 화면용)
if st.checkbox("리그 평균 지표 리포트 보기"):
    # full_data는 앞서 수집한 데이터프레임입니다.
    report = get_team_power_metrics(full_data)
    if report is not None:
        st.write("### 📊 핵심 지표 리그 평균 리포트")
        st.table(report)
    else:
        st.warning("데이터에 분석에 필요한 지표(속도, 배럴 등)가 없습니다.")
