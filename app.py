import streamlit as st
import numpy as np
import time
from datetime import datetime

# --- 1. 설정 및 데이터베이스 ---
team_db = {
    "bos": ["R.Devers", "J.Duran", "T.Casas", "M.Yoshida", "C.Rafaela", "D.Hamilton", "R.McGuire", "V.Abreu", "B.Wong"],
    "nyy": ["A.Judge", "J.Soto", "G.Torres", "A.Verdugo", "A.Volpe", "O.Cabrera", "J.Trevino", "D.LeMahieu", "A.Wells"]
}
player_to_team = {"r.devers": "bos", "a.judge": "nyy", "j.soto": "nyy"}

# --- 2. 분석 엔진 및 보정 로직 ---
def get_split_factor(player_id, is_hitting, is_home):
    return 1.05 if is_home else 0.95 

def analyze_absence_impact(team_id, player_name):
    """결장 임팩트 분석 로직"""
    # 임팩트 수치(예시): 0.15 (15% 감소)
    impact = 0.15 
    return impact, f"{player_name} 결장 시 팀의 득점 생산력이 {impact*100:.1f}% 감소하는 경향이 있습니다."

def analyze_split_adjusted_game(lineup, starter_id, is_home, absent_player=None):
    """보정 로직이 통합된 시뮬레이션"""
    total_lineup_power = sum([0.300 * get_split_factor(p, True, is_home) for p in lineup])
    
    # 결장자 임팩트 적용
    impact_comment = ""
    if absent_player:
        impact, impact_comment = analyze_absence_impact("team_id", absent_player)
        total_lineup_power *= (1 - impact)
        
    pitcher_factor = get_split_factor(starter_id, False, is_home)
    final_score = total_lineup_power / pitcher_factor
    return final_score, impact_comment

def generate_analysis_comment(team_name, calculated_win_prob, impact_comment):
    comment = f"\n### 📝 분석 리포트: {team_name}\n"
    comment += f"- 📉 **전력 누수 분석:** {impact_comment}\n"
    comment += f"- 📊 **최종 보정 승률:** {calculated_win_prob:.1%}"
    return comment

# --- 3. UI 구성 ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 코드", key="h_auto")
    absent = st.text_input("결장 선수 (없으면 공란)", key="absent_auto")
    if st.button("분석 실행 (자동)"):
        h_lineup = team_db.get(h_code.lower(), [])
        prob, i_comment = analyze_split_adjusted_game(h_lineup, "p_01", True, absent if absent else None)
        st.metric("최종 보정 승리 확률", f"{prob*100:.1f}%")
        st.write(generate_analysis_comment("홈 팀", prob, i_comment))

with tab2:
    h_man = st.text_area("홈 팀/선수 입력", key="h_man")
    absent_man = st.text_input("결장 선수", key="absent_man")
    if st.button("분석 실행 (수동)"):
        h_lineup = [p.strip() for p in h_man.split(',')]
        prob, i_comment = analyze_split_adjusted_game(h_lineup, "p_01", True, absent_man if absent_man else None)
        st.metric("최종 보정 승리 확률", f"{prob*100:.1f}%")
        st.write(generate_analysis_comment("홈 팀", prob, i_comment))
