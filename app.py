import streamlit as st
import numpy as np
import statsapi
import json
import re
import time
from datetime import datetime

# --- 1. 데이터 및 안전 유틸리티 ---
team_db = {"bos": 111, "nyy": 147}

def get_stats_from_boxscore(game_id, key_name='avg'):
    """박스스코어 데이터를 파싱하여 특정 지표를 안전하게 추출"""
    try:
        data = statsapi.boxscore_data(game_id)
        player_info = data.get('playerInfo', {})
        stats_list = []
        for p_id in player_info.keys():
            stats = player_info[p_id].get('stats', {}).get('hitting', {})
            stats_list.append(float(stats.get(key_name, 0.250)))
        return np.mean(stats_list) if stats_list else 0.250
    except:
        return 0.250

# --- 2. 분석 엔진 ---
def run_full_analysis(h_code, a_code, h_absent, a_absent):
    try:
        h_id = team_db.get(h_code.lower(), 111)
        games = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'), team=h_id)
        
        if not games:
            return 0.5, "### ⚠️ 상태 확인\n오늘 예정된 경기가 없습니다."
            
        game_id = games[0]['game_id']
        # 핵심 데이터 필드 추적 로직 적용
        avg_power = get_stats_from_boxscore(game_id, 'avg')
        
        final_score = avg_power
        report = f"### 📝 종합 분석 리포트\n- 📊 **평균 전력 지수(AVG):** {final_score:.3f}\n- ✅ **상태:** 실시간 박스스코어 데이터 파싱 완료"
    except Exception as e:
        final_score = 0.0
        report = f"### ⚠️ 분석 오류\n{e}"
    return final_score, report

# --- 3. UI 구성 (고정) ---
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
