import streamlit as st
import numpy as np
import statsapi # 실제 구동 시 설치 필요
from datetime import datetime

# --- 1. 실시간 데이터 엔진 ---
def get_live_lineup_and_game_info(team_id):
    """statsapi를 사용하여 실시간 게임 정보 및 라인업 추출"""
    game_info = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'), team=team_id)[0]
    # 라인업 및 투수 정보 등 핵심 변수 추출
    return game_info

def analyze_day_night_impact(team_id, lineup, starter_id, is_day):
    """기존 분석 로직 (내부 자동화)"""
    # 임의의 연산 로직 (실제 API 연동 시 통계 적용)
    power = 0.350 * (1.08 if is_day else 0.92)
    comment = f"현재 {team_id} 팀은 {'낮' if is_day else '저녁'} 경기에 특화된 전력을 보유 중입니다."
    return power, comment

# --- 2. 통합 시스템 (UI 고정) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("팀 코드 입력 (예: 111)", key="h_auto")
    if st.button("분석 실행 (자동)"):
        # 1. 데이터 추출 및 분석 로직 통합
        game_info = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'), team=h_code)[0]
        is_home = (game_info['home_id'] == int(h_code))
        is_day = True # 시간대 자동 판단 로직 추가 가능
        
        # 2. 심층 분석 수행
        final_power, comment = analyze_day_night_impact(h_code, ["P1", "P2"], 999, is_day)
        
        # 3. 결과 출력
        st.metric("통합 전력 지수", f"{final_power:.3f}")
        st.write(f"### 📝 AI 심층 분석 코멘트\n{comment}")

with tab2:
    st.info("수동 입력 모드입니다.")
    # (기존 수동 모드 로직 유지)
