import streamlit as st
import pandas as pd
import datetime

# --- 1. 백엔드 연산 로직 (화면 출력 없음) ---
@st.cache_data
def analyze_mlb_data(date, home, away):
    # 방금 수집하신 전체 Raw 데이터 로드
    df = pd.read_csv('full_mlb_events_2026.csv')
    
    # 여기서 날짜/팀을 기준으로 데이터 필터링 및 자동 연산
    # 예시: 특정 팀의 경기 데이터 매칭 (실제 컬럼명에 맞춰 수정 필요)
    match_data = df[(df['home_team'] == home) & (df['away_team'] == away)]
    
    if match_data.empty:
        return None
    
    # 분석된 결과값 산출
    return {
        'win_prob': 65.5, # 실제 연산값으로 교체 예정
        'avg_velocity': match_data['release_speed'].mean() if 'release_speed' in match_data.columns else 0,
        'launch_speed': match_data['launch_speed'].mean() if 'launch_speed' in match_data.columns else 0
    }

# --- 2. 메인 UI (프론트엔드) ---
st.title("⚾ MLB 승부 예측 분석기")

selected_date = st.date_input("경기 날짜 선택", datetime.date.today())
home_team = st.text_input("홈 팀 이름")
away_team = st.text_input("원정 팀 이름")

if st.button("분석 실행"):
    with st.spinner("데이터 분석 중..."):
        result = analyze_mlb_data(selected_date, home_team, away_team)
    
    if result:
        st.subheader("📊 최종 분석 결과")
        col1, col2, col3 = st.columns(3)
        col1.metric("승리 확률", f"{result['win_prob']}%")
        col2.metric("평균 투구 구속", f"{result['avg_velocity']:.1f} mph")
        col3.metric("평균 타구 속도", f"{result['launch_speed']:.1f} mph")
    else:
        st.warning("해당 팀의 데이터를 찾을 수 없습니다.")
