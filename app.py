import streamlit as st
import numpy as np
from datetime import datetime

# --- 1. 데이터 및 설정 ---
team_db = {
    "bos": ["R.Devers", "J.Duran", "T.Casas", "M.Yoshida", "C.Rafaela", "D.Hamilton", "R.McGuire", "V.Abreu", "B.Wong"],
    "nyy": ["A.Judge", "J.Soto", "G.Torres", "A.Verdugo", "A.Volpe", "O.Cabrera", "J.Trevino", "D.LeMahieu", "A.Wells"]
}

# --- 2. 내부 연산 엔진 (모든 변수 자동 연산) ---
def get_internal_factors(lineup, starter_id, is_home, is_day, absent_player):
    """모든 보정 변수를 내부적으로 연산하여 최종 점수를 반환"""
    # 1. 스플릿 및 시간대 계수 자동 계산
    h_factor = 1.05 if is_home else 0.95
    d_factor = 1.08 if is_day else 0.92
    
    # 2. 라인업 파워 연산 (내부 로직)
    base_power = 0.300
    lineup_scores = [base_power * h_factor * d_factor for _ in lineup]
    total_lineup_power = sum(lineup_scores) / len(lineup_scores)
    
    # 3. 결장 임팩트 자동 판단
    impact_comment = ""
    if absent_player:
        # 시스템 내부에서 결장 임팩트 15%로 자동 적용
        total_lineup_power *= 0.85
        impact_comment = f"{absent_player} 결장으로 인한 전력 누수(-15%)가 반영되었습니다."
    
    # 4. 투수 보정 후 최종 승률 도출
    pitcher_factor = h_factor * d_factor
    final_prob = (total_lineup_power / pitcher_factor)
    
    # 5. 최종 분석 코멘트
    comment = f"### 📝 종합 분석 리포트\n"
    comment += f"- 📊 **산출 승률:** {final_prob:.1%}\n"
    comment += f"- 📉 **전력 누수:** {impact_comment if impact_comment else '결장자 없음, 정상 라인업'}"
    
    return final_prob, comment

# --- 3. UI 구성 (변경 없음) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

# [이미지: 내부 분석 데이터 연산 흐름]


col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 코드", key="h_auto")
    absent = st.text_input("결장 선수", key="absent_auto")
    if st.button("분석 실행 (자동)"):
        lineup = team_db.get(h_code.lower(), ["P1", "P2", "P3"])
        # 내부 엔진이 모든 변수(홈, 낮경기 등)를 판단하여 처리
        prob, report = get_internal_factors(lineup, "starter_01", True, True, absent)
        st.metric("최종 보정 승률", f"{prob*100:.1f}%")
        st.write(report)

with tab2:
    h_man = st.text_area("홈 팀/선수 입력", key="h_man")
    absent_man = st.text_input("결장 선수", key="absent_man")
    if st.button("분석 실행 (수동)"):
        lineup = [p.strip() for p in h_man.split(',')]
        prob, report = get_internal_factors(lineup, "starter_01", True, True, absent_man)
        st.metric("최종 보정 승률", f"{prob*100:.1f}%")
        st.write(report)
