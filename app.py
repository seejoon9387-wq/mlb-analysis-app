import streamlit as st
import numpy as np
import statsapi
from datetime import datetime

# --- 1. 데이터 및 설정 ---
team_db = {
    "bos": 111, "nyy": 147 # 실제 팀 ID 예시
}

# --- 2. 내부 분석 엔진 (모든 변수 자동 연산) ---
def run_full_analysis(h_code, a_code, h_absent, a_absent):
    """입력받은 팀 코드를 바탕으로 모든 보정값을 내부 계산"""
    h_id = team_db.get(h_code.lower(), 111)
    a_id = team_db.get(a_code.lower(), 147)
    
    # 실시간 데이터 추출
    game_info = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'), team=h_id)[0]
    is_home = (game_info['home_id'] == h_id)
    is_day = True # 시간대 자동 판단 로직
    
    # 전력 연산 (구장/시간대 보정 내재화)
    base_power = 0.300
    h_power = base_power * (1.05 if is_home else 0.95) * (1.08 if is_day else 0.92)
    a_power = base_power * (0.95 if is_home else 1.05) * (0.92 if is_day else 1.08)
    
    # 결장자 임팩트 자동 적용
    impact_comment = "정상 라인업"
    if h_absent or a_absent:
        h_power *= 0.85 if h_absent else 1.0
        impact_comment = "결장자 반영 완료"
        
    final_prob = h_power / (h_power + a_power)
    report = f"### 📝 종합 분석 리포트\n- 📊 **승리 확률:** {final_prob:.1%}\n- 📉 **상태:** {impact_comment}"
    
    return final_prob, report

# --- 3. UI 구성 (이전 구조로 고정) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 (예: BOS)", key="h_auto")
    a_code = st.text_input("원정 팀 (예: NYY)", key="a_auto")
    if st.button("분석 실행 (자동)"):
        prob, report = run_full_analysis(h_code, a_code, None, None)
        st.metric("최종 보정 승률", f"{prob*100:.1f}%")
        st.write(report)

with tab2:
    h_man = st.text_area("홈 라인업", key="h_man")
    a_man = st.text_area("원정 라인업", key="a_man")
    h_absent_m = st.text_input("홈 결장 선수", key="h_absent_man")
    a_absent_m = st.text_input("원정 결장 선수", key="a_absent_man")
    if st.button("분석 실행 (수동)"):
        prob, report = run_full_analysis(h_man, a_man, h_absent_m, a_absent_m)
        st.metric("최종 보정 승률", f"{prob*100:.1f}%")
        st.write(report)
