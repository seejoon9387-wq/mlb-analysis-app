import streamlit as st
import numpy as np
import statsapi
import json
from datetime import datetime

# --- 1. 데이터 파싱 및 전력 계산 핵심 엔진 ---
def parse_stats_string(stats_str):
    """텍스트형 통계 데이터를 구조화된 딕셔너리로 변환"""
    stats_dict = {}
    if not isinstance(stats_str, str): return stats_dict
    for line in stats_str.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            stats_dict[key.strip()] = value.strip()
    return stats_dict

def get_team_power_score(lineup_names):
    """선수 명단으로 평균 OPS를 계산하는 로직"""
    total_power, valid_players = 0, 0
    for name in lineup_names:
        results = statsapi.lookup_player(name)
        if not results: continue
        stats_str = statsapi.player_stats(results[0]['id'], group='hitting', type='season')
        stats_data = parse_stats_string(stats_str)
        if 'ops' in stats_data:
            total_power += float(stats_data['ops'])
            valid_players += 1
    return total_power / valid_players if valid_players > 0 else 0

# --- 2. 통합 분석 로직 (내부 엔진) ---
def run_analysis_process(lineup_input):
    """내부에서 모든 로직을 자동 연산"""
    names = [p.strip() for p in lineup_input.split(',')]
    score = get_team_power_score(names)
    return score

# --- 3. UI 고정 (이전 구조와 동일) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

# [상단 설정창 고정]
col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

# [2개 탭 구성 고정]
tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 코드", key="h_auto")
    a_code = st.text_input("원정 팀 코드", key="a_auto")
    if st.button("분석 실행 (자동)"):
        # 내부 엔진 연산
        score = run_analysis_process("Rafael Devers, Jarren Duran") # 예시 라인업
        st.metric("최종 보정 승률", f"{score*100:.1f}%")
        st.write("### 📝 종합 분석 리포트\n내부 연산이 완료되었습니다.")

with tab2:
    h_man = st.text_area("홈 팀/선수 입력", key="h_man")
    a_man = st.text_area("원정 팀/선수 입력", key="a_man")
    h_absent_m = st.text_input("홈 결장 선수", key="h_absent_man")
    a_absent_m = st.text_input("원정 결장 선수", key="a_absent_man")
    if st.button("분석 실행 (수동)"):
        score = run_analysis_process(h_man)
        st.metric("최종 보정 승률", f"{score*100:.1f}%")
        st.write("### 📝 정밀 분석 완료")
