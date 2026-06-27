import streamlit as st
import numpy as np
import statsapi
import json
from datetime import datetime, timedelta

# --- 1. 데이터 및 안전 유틸리티 ---
team_db = {"bos": 111, "nyy": 147}

def get_safe_stat(stats_data, key):
    if isinstance(stats_data, str):
        try: stats_data = json.loads(stats_data)
        except: stats_data = {}
    return stats_data.get(key, 0.0) if isinstance(stats_data, dict) else 0.0

# --- 2. 내부 분석 엔진 (경기 상태 확인 로직 포함) ---
def run_full_analysis(h_code, a_code, h_absent, a_absent):
    try:
        h_id = team_db.get(h_code.lower(), 111)
        # 1. 경기 일정 및 상태 확인 로직
        schedule = statsapi.schedule(start_date='2026-06-27', end_date='2026-06-28', team=h_id)
        
        if not schedule:
            return 0.5, "### ⚠️ 상태 확인\n해당 기간에 예정된 경기가 없습니다."
            
        # 상태 확인 및 데이터 추출
        game = schedule[0]
        status = game['status']
        if status == 'Postponed':
            return 0.5, f"### ⚠️ 경기 상태: {status}\n경기가 연기되어 분석을 수행할 수 없습니다."
        
        # 2. 보정 로직 (상태 확인 통과 시)
        h_power = get_safe_stat('{"avg": 0.310}', 'avg')
        a_power = 0.280
        if h_absent: h_power *= 0.85
            
        final_prob = h_power / (h_power + a_power)
        report = f"### 📝 종합 분석 리포트\n- 📅 **경기 날짜:** {game['game_date']}\n- 📊 **승리 확률:** {final_prob:.1%}\n- ✅ **상태:** {status}"
        
    except Exception as e:
        final_prob = 0.5
        report = f"### ⚠️ 분석 오류\n데이터 처리 중 문제가 발생했습니다: {e}"
    
    return final_prob, report

# --- 3. UI 구성 (고정) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime(2026, 6, 27))
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
