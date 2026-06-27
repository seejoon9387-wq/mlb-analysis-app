import streamlit as st
import pandas as pd
import requests
from datetime import date

# 페이지 설정
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 정밀 분석 시스템")

# 데이터 보존을 위한 세션 상태
if 'analyzed_data' not in st.session_state:
    st.session_state['analyzed_data'] = None

# [분석 엔진 함수]
def run_analysis(player_id):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": player_id}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json().get('body', {})
        opponents = data.get('opponents', [])
        
        all_data = []
        for item in opponents:
            if isinstance(item, list): all_data.extend(item)
            else: all_data.append(item)
            
        if all_data:
            st.session_state['analyzed_data'] = pd.json_normalize(all_data)
            return True
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
    return False

# --- UI 및 레이아웃 ---
left_col, right_col = st.columns([1, 2])

with left_col:
    st.header("⚙️ 분석 환경 설정")
    
    # 입력 컴포넌트들을 항상 유지
    player_id = st.text_input("분석할 선수 ID", value="592450")
    target_date = st.date_input("분석 기준 날짜", value=date.today())
    date_range = st.slider("데이터 조회 범위 (최근 N일)", 1, 30, 7)
    
    st.divider()
    
    tab1, tab2 = st.tabs(["⚡ 자동 분석", "🔍 수동 분석"])
    
    with tab1:
        if st.button("자동 분석 시작", type="primary"):
            with st.spinner("데이터 수집 중..."):
                run_analysis(player_id)
                st.rerun() # 데이터를 가져온 후 화면을 갱신하여 결과 출력
            
    with tab2:
        h_roster = st.text_area("홈 팀 명단")
        a_roster = st.text_area("원정 팀 명단")
        if st.button("정밀 분석 엔진 가동"):
            st.info("수동 분석 엔진 활성화 중...")

with right_col:
    st.subheader("📊 분석 결과 및 통계 리포트")
    
    if st.session_state['analyzed_data'] is not None:
        df = st.session_state['analyzed_data']
        cols = [c for c in ['batterName', 'pitcherName', 'H', 'AB', 'AVG', 'OPS', 'HR'] if c in df.columns]
        st.dataframe(df[cols].sort_values(by='OPS', ascending=False), use_container_width=True)
        
        if st.button("결과 초기화"):
            st.session_state['analyzed_data'] = None
            st.rerun()
    else:
        st.info("좌측에서 설정값을 입력하고 '자동 분석 시작'을 누르세요.")

st.divider()
st.caption("AI Analyst System v1.0 | 상태: " + ("데이터 로드 완료" if st.session_state['analyzed_data'] is not None else "대기중"))
