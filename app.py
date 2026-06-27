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
    """홈/원정 성적에 따른 보정 계수 반환 (예시값)"""
    # 실제 환경에서는 API 데이터 연동
    return 1.05 if is_home else 0.95 

def resolve_lineup(user_input):
    user_input = user_input.lower().strip()
    if user_input in team_db: return team_db[user_input]
    if user_input in player_to_team: return team_db[player_to_team[user_input]]
    return [p.strip() for p in user_input.split(',')]

def analyze_split_adjusted_game(lineup, starter_id, is_home):
    """보정 로직이 통합된 시뮬레이션"""
    total_lineup_power = sum([0.300 * get_split_factor(p, True, is_home) for p in lineup])
    pitcher_factor = get_split_factor(starter_id, False, is_home)
    
    # 코멘트 생성
    if pitcher_factor < 0.9:
        comment = "투수가 오늘 경기장에서 매우 강한(낮은 방어율) 기록을 가지고 있습니다."
    elif pitcher_factor > 1.1:
        comment = "투수가 오늘 경기장에서 다소 취약한(높은 방어율) 경향이 발견되었습니다."
    else:
        comment = "홈/원정 보정 결과, 투수진의 기복은 평이합니다."
        
    final_score = total_lineup_power / pitcher_factor
    return final_score, comment

def generate_analysis_comment(team_name, power_score, calculated_win_prob, pitcher_comment):
    comment = f"\n### 📝 분석 리포트: {team_name}\n"
    comment += f"- ⚾ **투수 기록 보정:** {pitcher_comment}\n"
    comment += f"- 📊 **산출 승률:** {calculated_win_prob:.1%}"
    return comment

# --- 3. UI 구성 ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 코드 (예: BOS)", key="h_auto")
    a_code = st.text_input("원정 팀 코드 (예: NYY)", key="a_auto")
    if st.button("분석 실행 (자동)"):
        h_lineup = team_db.get(h_code.lower(), [])
        prob, p_comment = analyze_split_adjusted_game(h_lineup, "p_01", True)
        st.metric("홈 팀 보정 승리 확률", f"{prob*100:.1f}%")
        st.write(generate_analysis_comment("홈 팀", 0.360, prob, p_comment))

with tab2:
    h_man = st.text_area("홈 팀/선수 입력", key="h_man")
    a_man = st.text_area("원정 팀/선수 입력", key="a_man")
    if st.button("분석 실행 (수동)"):
        h_lineup = resolve_lineup(h_man)
        a_lineup = resolve_lineup(a_man)
        prob, p_comment = analyze_split_adjusted_game(h_lineup, "p_01", True)
        st.metric("홈 팀 보정 승리 확률", f"{prob*100:.1f}%")
        st.write(generate_analysis_comment("홈 팀", 0.360, prob, p_comment))
