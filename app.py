import streamlit as st
import numpy as np
import statsapi
import json
import re
from datetime import datetime

# --- 1. 안전 파싱 및 전력 계산 유틸리티 ---
def parse_stats_string(stats_str):
    """문자열 형태의 스탯 데이터를 딕셔너리로 안전하게 변환"""
    try:
        if isinstance(stats_str, str): return json.loads(stats_str)
        return stats_str if isinstance(stats_str, dict) else {}
    except: return {}

def calculate_team_power_safe(stats_list):
    """수집된 선수들의 스탯으로 팀 전력 점수 산출"""
    if not stats_list: return 0.0
    # 예시: 타율(avg) 기반 계산
    scores = [float(s.get('avg', 0.250)) for s in stats_list if s.get('avg')]
    return np.mean(scores) if scores else 0.250

# --- 2. 내부 분석 엔진 ---
def run_full_analysis(team_id):
    """팀 ID를 받아 로스터 파싱부터 점수 계산까지 자동화"""
    try:
        # 1. 로스터 가져오기
        roster_str = statsapi.roster(team_id)
        player_names = []
        for line in roster_str.split('\n'):
            match = re.search(r'#\d+\s+(\S+\s+){0,2}(.+)', line)
            if match: player_names.append(match.group(2).strip())
        
        # 2. 선수별 데이터 파싱
        lineup_stats = []
        for name in player_names[:9]:
            results = statsapi.lookup_player(name)
            if results:
                p_id = results[0]['id']
                s_str = statsapi.player_stats(p_id, group='hitting', type='season')
                lineup_stats.append(parse_stats_string(s_str))
        
        # 3. 점수 계산
        final_score = calculate_team_power_safe(lineup_stats)
        return final_score, f"총 {len(lineup_stats)}명의 선수 데이터 분석 완료."
    except Exception as e:
        return 0.0, f"분석 오류: {e}"

# --- 3. UI 구성 (고정) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    # 팀 ID 111 (보스턴) 자동 분석
    if st.button("보스턴 로스터 자동 분석"):
        score, report = run_full_analysis(111)
        st.metric("보스턴 평균 전력 지수", f"{score:.3f}")
        st.write(f"### 📝 분석 결과\n{report}")

with tab2:
    st.info("수동 분석 모드입니다.")
    # 기존 수동 로직 유지...
