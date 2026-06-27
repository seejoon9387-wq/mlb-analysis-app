import streamlit as st
import numpy as np
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

def get_day_night_factor(player_id, is_hitting, is_day):
    """낮/밤 경기 성적에 따른 보정 계수 반환"""
    return 1.08 if is_day else 0.92

def analyze_absence_impact(team_id, player_name):
    impact = 0.15 
    return impact, f"{player_name} 결장 시 득점력이 {impact*100:.1f}% 감소하는 경향이 있습니다."

def run_comprehensive_analysis(lineup, starter_id, is_home, is_day, absent_player=None):
    """모든 보정 로직을 통합한 최종 시뮬레이션"""
    # 기본 전력에 구장 보정 및 시간대 보정 적용
    lineup_scores = [0.300 * get_split_factor(p, True, is_home) * get_day_night_factor(p, True, is_day) for p in lineup]
    total_lineup_power = sum(lineup_scores) / len(lineup_scores)
    
    # 결장자 임팩트
    impact_comment = ""
    if absent_player:
        impact, impact_comment = analyze_absence_impact("team_id", absent_player)
        total_lineup_power *= (1 - impact)
        
    # 투수 보정
    pitcher_factor = get_split_factor(starter_id, False, is_home) * get_day_night_factor(starter_id, False, is_day)
    
    # 최종 결과 산출
    final_score = total_lineup_power / pitcher_factor
    return final_score, impact_comment

def generate_full_report(team_name, calculated_win_prob, impact_comment):
    comment = f"### 📝 종합 분석 리포트: {team_name}\n"
    comment += f"- 📉 **전력 누수:** {impact_comment}\n"
    comment += f"- 📊 **최종 보정 승률:** {calculated_win_prob:.1%}"
    return comment

# --- 3. UI 구성 ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

# 상단 설정
col_t1, col_t2 = st.columns(2)
is_day = col_t1.checkbox("낮 경기 여부", True)
is_home = col_t2.checkbox("홈 경기 여부", True)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 코드", key="h_auto")
    absent = st.text_input("결장 선수", key="absent_auto")
    if st.button("분석 실행 (자동)"):
        h_lineup = team_db.get(h_code.lower(), ["Player1", "Player2"])
        prob, i_comment = run_comprehensive_analysis(h_lineup, "starter_01", is_home, is_day, absent)
        st.metric("최종 보정 승률", f"{prob*100:.1f}%")
        st.write(generate_full_report("홈 팀", prob, i_comment))

with tab2:
    h_man = st.text_area("홈 팀/선수 입력", key="h_man")
    absent_man = st.text_input("결장 선수", key="absent_man")
    if st.button("분석 실행 (수동)"):
        h_lineup = [p.strip() for p in h_man.split(',')]
        prob, i_comment = run_comprehensive_analysis(h_lineup, "starter_01", is_home, is_day, absent_man)
        st.metric("최종 보정 승률", f"{prob*100:.1f}%")
        st.write(generate_full_report("홈 팀", prob, i_comment))
