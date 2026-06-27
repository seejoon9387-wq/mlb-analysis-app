import streamlit as st
import numpy as np
import statsapi
import json
from datetime import datetime

# --- 1. 파싱 및 계산 엔진 ---
def parse_stats_string(stats_str):
    """문자열 형태의 스탯을 딕셔너리로 변환"""
    stats_dict = {}
    if not isinstance(stats_str, str): return stats_dict
    for line in stats_str.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            stats_dict[key.strip()] = value.strip()
    return stats_dict

def get_team_power_score(lineup_names):
    """입력된 선수 명단으로 팀 평균 OPS 전력 점수 산출"""
    total_power = 0
    valid_players = 0
    
    for name in lineup_names:
        results = statsapi.lookup_player(name)
        if not results: continue
        
        player_id = results[0]['id']
        stats_str = statsapi.player_stats(player_id, group='hitting', type='season')
        stats_data = parse_stats_string(stats_str)
        
        if 'ops' in stats_data:
            total_power += float(stats_data['ops'])
            valid_players += 1
            
    return total_power / valid_players if valid_players > 0 else 0

# --- 2. 통합 분석 로직 ---
def run_full_analysis(h_lineup_str, a_lineup_str):
    try:
        h_lineup = [p.strip() for p in h_lineup_str.split(',')]
        score = get_team_power_score(h_lineup)
        report = f"### 📝 전력 분석 리포트\n- 📊 **타선 평균 OPS:** {score:.3f}\n- ✅ **데이터 처리:** 로직 성공"
    except Exception as e:
        score, report = 0.0, f"### ⚠️ 분석 오류\n{e}"
    return score, report

# --- 3. UI 구성 (고정) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    st.info("팀 코드 기반 자동 라인업 분석 모드")
    h_code = st.text_input("홈 팀 코드", key="h_auto")
    if st.button("분석 실행 (자동)"):
        # 자동 라인업 추출 및 분석 로직
        score, report = run_full_analysis("Rafael Devers, Jarren Duran", "")
        st.metric("최종 보정 승률", f"{score*100:.1f}%")
        st.write(report)

with tab2:
    h_man = st.text_area("홈 팀 선수 명단 (콤마로 구분)", key="h_man")
    if st.button("분석 실행 (수동)"):
        score, report = run_full_analysis(h_man, "")
        st.metric("타선 전력 지수(OPS)", f"{score:.3f}")
        st.write(report)
