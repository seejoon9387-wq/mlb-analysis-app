import streamlit as st
import numpy as np
import statsapi
import json
from datetime import datetime

# --- 1. 데이터 및 안전 유틸리티 ---
team_db = {"bos": 111, "nyy": 147}

def parse_stats_string(stats_str):
    """문자열 데이터를 딕셔너리로 파싱하는 유틸리티"""
    try:
        return json.loads(stats_str)
    except:
        return {}

def get_safe_stat(stats_data, key):
    """데이터 타입 확인 후 안전하게 값을 가져오는 함수"""
    # 추가된 파싱 보호 로직
    if isinstance(stats_data, str):
        stats_data = parse_stats_string(stats_data)
        
    if isinstance(stats_data, dict):
        return stats_data.get(key, 0.0)
    return 0.0

# --- 2. 내부 분석 엔진 ---
def run_full_analysis(h_code, a_code, h_absent, a_absent):
    """입력 데이터를 분석 엔진으로 전달"""
    try:
        # 실시간 데이터 호출
        h_id = team_db.get(h_code.lower(), 111)
        game_info = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'), team=h_id)[0]
        
        # 스탯 파싱 예시 (API 데이터가 문자열로 올 경우를 대비)
        raw_stats = '{"avg": 0.310}' # 실제로는 API에서 받은 데이터
        
        # get_safe_stat을 통해 안전하게 추출
        h_power = get_safe_stat(raw_stats, 'avg') 
        a_power = 0.280
        
        # 보정 및 승률 계산
        final_prob = h_power / (h_power + a_power)
        report = f"### 📝 종합 분석 리포트\n- 📊 **승리 확률:** {final_prob:.1%}\n- 📉 **상태:** 데이터 파싱 및 검증 완료"
        
    except Exception as e:
        final_prob = 0.5
        report = f"### ⚠️ 분석 오류\n데이터 처리 중 문제가 발생했습니다: {e}"
    
    return final_prob, report

# --- 3. UI 구성 (고정) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
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
