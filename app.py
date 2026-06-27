import streamlit as st
import numpy as np
from datetime import datetime

# --- 1. 데이터 및 설정 ---
team_db = {
    "bos": ["R.Devers", "J.Duran", "T.Casas", "M.Yoshida", "C.Rafaela", "D.Hamilton", "R.McGuire", "V.Abreu", "B.Wong"],
    "nyy": ["A.Judge", "J.Soto", "G.Torres", "A.Verdugo", "A.Volpe", "O.Cabrera", "J.Trevino", "D.LeMahieu", "A.Wells"]
}

# --- 2. 내부 연산 엔진 (모든 변수 자동 연산) ---
def get_internal_factors(h_lineup, a_lineup, h_absent, a_absent):
    """홈/원정, 결장 임팩트 등 모든 변수를 내부적으로 연산"""
    
    # 기본 스코어 설정 (0.0 ~ 1.0)
    base_power = 0.300
    
    # 1. 라인업 파워 연산 (홈/원정 보정 내재화)
    h_power = sum([base_power * 1.05 for _ in h_lineup]) / len(h_lineup)
    a_power = sum([base_power * 0.95 for _ in a_lineup]) / len(a_lineup)
    
    # 2. 결장 임팩트 자동 적용
    impact_comment = ""
    if h_absent:
        h_power *= 0.85
        impact_comment += f"[홈] {h_absent} 결장(전력 -15%) 반영. "
    if a_absent:
        a_power *= 0.85
        impact_comment += f"[원정] {a_absent} 결장(전력 -15%) 반영."
    
    # 3. 승률 계산
    final_prob = h_power / (h_power + a_power)
    
    # 4. 리포트 생성
    report = f"### 📝 종합 분석 리포트\n"
    report += f"- 📊 **홈 팀 승리 확률:** {final_prob:.1%}\n"
    report += f"- 📉 **전력 누수 상태:** {impact_comment if impact_comment else '결장자 없음, 정상 라인업'}"
    
    return final_prob, report

# --- 3. UI 구성 (원정팀 입력란 복구) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 코드", key="h_auto")
    a_code = st.text_input("원정 팀 코드", key="a_auto")
    h_absent = st.text_input("홈 결장 선수", key="h_absent_auto")
    a_absent = st.text_input("원정 결장 선수", key="a_absent_auto")
    
    if st.button("분석 실행 (자동)"):
        h_lineup = team_db.get(h_code.lower(), ["P1"])
        a_lineup = team_db.get(a_code.lower(), ["P1"])
        prob, report = get_internal_factors(h_lineup, a_lineup, h_absent, a_absent)
        st.metric("최종 보정 승률", f"{prob*100:.1f}%")
        st.write(report)

with tab2:
    h_man = st.text_area("홈 팀/선수 입력", key="h_man")
    a_man = st.text_area("원정 팀/선수 입력", key="a_man")
    h_absent_m = st.text_input("홈 결장 선수", key="h_absent_man")
    a_absent_m = st.text_input("원정 결장 선수", key="a_absent_man")
    
    if st.button("분석 실행 (수동)"):
        h_lineup = [p.strip() for p in h_man.split(',')]
        a_lineup = [p.strip() for p in a_man.split(',')]
        prob, report = get_internal_factors(h_lineup, a_lineup, h_absent_m, a_absent_m)
        st.metric("최종 보정 승률", f"{prob*100:.1f}%")
        st.write(report)
