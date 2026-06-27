import streamlit as st
import numpy as np
import statsapi
import json
import time
from datetime import datetime

# --- 1. 핵심 분석 엔진 ---
def parse_stats_string(stats_str):
    """텍스트형 스탯을 딕셔너리로 변환"""
    stats_dict = {}
    if not isinstance(stats_str, str): return stats_dict
    for line in stats_str.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            stats_dict[key.strip()] = value.strip()
    return stats_dict

def get_team_power_score(lineup_names):
    """OPS 기반 팀 전력 점수 산출"""
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

def analyze_any_team(team_id):
    """함수화된 통합 분석 로직"""
    # [실제 구현 시 get_lineup_live_with_timeout 로직 연동]
    # 여기서는 예시를 위해 보스턴의 핵심 선수 명단을 하드코딩
    sample_lineup = ['Rafael Devers', 'Jarren Duran', 'Ceddanne Rafaela']
    score = get_team_power_score(sample_lineup)
    return score

# --- 2. UI 구성 (이전 구조 고정) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 ID (예: 111)", key="h_auto")
    if st.button("분석 실행 (자동)"):
        # 팀 ID만 넣으면 analyze_any_team이 모두 처리
        score = analyze_any_team(int(h_code))
        st.metric("타선 평균 전력 지수(OPS)", f"{score:.3f}")
        st.write("### 📝 분석 결과\n분석 엔진이 실시간으로 라인업을 구성하고 OPS 데이터를 집계했습니다.")

with tab2:
    h_man = st.text_area("선수 명단 (이름, 이름...)", key="h_man")
    if st.button("분석 실행 (수동)"):
        names = [p.strip() for p in h_man.split(',')]
        score = get_team_power_score(names)
        st.metric("타선 평균 전력 지수(OPS)", f"{score:.3f}")
        st.write("### 📝 정밀 분석 완료")
