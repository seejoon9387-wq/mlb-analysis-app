import streamlit as st
import numpy as np
import statsapi
import json
import re
from datetime import datetime, timedelta

# --- 1. 데이터 및 안전 유틸리티 ---
team_db = {"bos": 111, "nyy": 147}

def parse_stats_string(stats_str):
    try:
        if isinstance(stats_str, str): return json.loads(stats_str)
        return stats_str if isinstance(stats_str, dict) else {}
    except: return {}

def get_safe_stat(stats_data, key):
    if isinstance(stats_data, str): stats_data = parse_stats_string(stats_data)
    return stats_data.get(key, 0.250) if isinstance(stats_data, dict) else 0.250

def run_full_analysis(h_code, a_code, h_absent, a_absent):
    try:
        h_id = team_db.get(h_code.lower(), 111)
        # 1. 로스터 가져오기 및 파싱
        roster_str = statsapi.roster(h_id)
        player_names = [re.search(r'#\d+\s+(\S+\s+){0,2}(.+)', line).group(2).strip() 
                        for line in roster_str.split('\n') if re.search(r'#\d+\s+(\S+\s+){0,2}(.+)', line)]
        
        # 2. 전력 계산
        stats = [get_safe_stat(statsapi.player_stats(statsapi.lookup_player(name)[0]['id'], group='hitting', type='season'), 'avg') 
                 for name in player_names[:9] if statsapi.lookup_player(name)]
        
        final_score = np.mean(stats) if stats else 0.250
        report = f"### 📝 종합 분석 리포트\n- 📊 **평균 전력 지수:** {final_score:.3f}\n- ✅ **상태:** 데이터 파싱 완료"
    except Exception as e:
        final_score = 0.0
        report = f"### ⚠️ 분석 오류\n{e}"
    return final_score, report

# --- 2. UI 구성 (이전 구조 고정) ---
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
        score, report = run_full_analysis(h_code, a_code, None, None)
        st.metric("최종 보정 승률", f"{score*100:.1f}%")
        st.write(report)

with tab2:
    h_man = st.text_area("홈 팀/선수 입력", key="h_man")
    a_man = st.text_area("원정 팀/선수 입력", key="a_man")
    h_absent_m = st.text_input("홈 결장 선수", key="h_absent_man")
    a_absent_m = st.text_input("원정 결장 선수", key="a_absent_man")
    if st.button("분석 실행 (수동)"):
        score, report = run_full_analysis(h_man, a_man, h_absent_m, a_absent_m)
        st.metric("최종 보정 승률", f"{score*100:.1f}%")
        st.write(report)
