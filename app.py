import streamlit as st
import pandas as pd
import datetime

# --- 1. 백그라운드 데이터 로드 및 연산 (화면 출력 없음) ---
@st.cache_data # 파일 로딩 속도를 위해 캐싱 사용
def load_and_analyze(home, away):
    # CSV에서 데이터 읽기
    df = pd.read_csv('savant_pitcher_2024_2026.csv')
    
    # 2026년 최신 데이터만 필터링하고 연산 (백그라운드 처리)
    # 예: 팀별 평균 FIP 추출 로직
    # (실제 데이터 컬럼명에 맞춰 수정 필요)
    result = {
        'win_prob': 65.5, # 예시 계산값
        'fip': df['fip'].mean() if 'fip' in df.columns else 0.0,
        'whiff': df['whiff_pct'].mean() if 'whiff_pct' in df.columns else 0.0
    }
    return result

# --- 2. 메인 화면 로직 (결과 표시 위주) ---
st.title("⚾ MLB 승부 예측 분석기")

selected_date = st.date_input("경기 날짜 선택", datetime.date.today())
home_team = st.text_input("홈 팀 이름")
away_team = st.text_input("원정 팀 이름")

if st.button("분석 실행"):
    with st.spinner("데이터 분석 중..."):
        # 로직 호출
        data = load_and_analyze(home_team, away_team)
    
    # 3. 결과 표시 (요약 정보만)
    st.subheader("📊 최종 분석 결과")
    col1, col2, col3 = st.columns(3)
    col1.metric("승리 확률", f"{data['win_prob']}%")
    col2.metric("선발투수 FIP", f"{data['fip']:.2f}")
    col3.metric("선발투수 Whiff %", f"{data['whiff']:.1f}%")
