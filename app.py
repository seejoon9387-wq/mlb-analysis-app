import streamlit as st
import pandas as pd
import requests
from datetime import date

# 페이지 설정
st.set_page_config(page_title="MLB AI Analyst", layout="wide")
st.title("⚾ MLB AI 정밀 분석 시스템")

# 데이터 관리: 세션 상태에 저장하여 데이터 유지
if 'analyzed_data' not in st.session_state:
    st.session_state['analyzed_data'] = None

# [분석 엔진 함수]
def run_analysis(player_id):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": player_id}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get('body', {})
    opponents = data.get('opponents', [])
    
    all_data = []
    for item in opponents:
        if isinstance(item, list): all_data.extend(item)
        else: all_data.append(item)
    
    if all_data:
        df = pd.json_normalize(all_data)
        st.session_state['analyzed_data'] = df
        return True
    return False

# --- 레이아웃 ---
left_col, right_col = st.columns([1, 2])

with left_col:
    st.header("⚙️ 분석 환경 설정")
    player_id = st.text_input("분석할 선수 ID", value="592450")
    target_date = st.date_input("분석 기준 날짜", value=date.today())
    date_range = st.slider("데이터 조회 범위 (최근 N일)", 1, 30, 7)
    
    st.divider()
    
    tab1, tab2 = st.tabs(["⚡ 자동 분석", "🔍 수동 분석"])
    
    with tab1:
        if st.button("자동 분석 시작", type="primary"):
            with st.spinner("데이터 수집 및 분석 중..."):
                if run_analysis(player_id):
                    st.success("데이터 로드 완료!")
                else:
                    st.error("데이터를 가져올 수 없습니다.")

with right_col:
    st.subheader("📊 분석 결과 및 통계 리포트")
    
    if st.session_state['analyzed_data'] is not None:
        df = st.session_state['analyzed_data']
        
        # 핵심 컬럼 추출 및 정렬
        cols = [c for c in ['batterName', 'pitcherName', 'H', 'AB', 'AVG', 'OPS', 'HR'] if c in df.columns]
        st.dataframe(df[cols].sort_values(by='OPS', ascending=False), use_container_width=True)
        
        if st.button("분석 결과 초기화"):
            st.session_state['analyzed_data'] = None
            st.rerun()
    else:
        st.info("좌측에서 선수 ID를 입력하고 '자동 분석 시작'을 누르세요.")

st.divider()
st.caption("AI Analyst System v1.0 | 데이터 최적화 상태: " + ("로드됨" if st.session_state['analyzed_data'] is not None else "대기중"))
