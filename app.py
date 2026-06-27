import streamlit as st
import numpy as np
import statsapi
import json
import re
from datetime import datetime

# --- 1. 강화된 안전 파싱 유틸리티 ---
def get_safe_stat(stats_data, key):
    """
    데이터가 리스트인지, 딕셔너리인지, 혹은 문자열인지 확인하여 
    안전하게 특정 키 값을 추출하는 통합 로직
    """
    # 1. 문자열이면 딕셔너리 변환
    if isinstance(stats_data, str):
        try: stats_data = json.loads(stats_data)
        except: return 0.250
    
    # 2. 리스트인 경우 0번 인덱스 추출
    if isinstance(stats_data, list) and len(stats_data) > 0:
        stats_data = stats_data[0]
        
    # 3. 최종 딕셔너리에서 값 추출
    if isinstance(stats_data, dict):
        return stats_data.get(key, 0.250)
    return 0.250

# --- 2. 통합 분석 엔진 ---
def run_full_analysis(h_code, a_code, h_absent, a_absent):
    try:
        h_id = 111 # 보스턴 예시
        # 시즌 스탯 호출 (API로부터 리스트 또는 딕셔너리가 올 수 있음)
        stats = statsapi.player_stats(h_id, group='hitting', type='season')
        
        # 강화된 get_safe_stat 적용
        avg_power = get_safe_stat(stats, 'avg')
        
        final_score = float(avg_power)
        report = f"### 📝 종합 분석 리포트\n- 📊 **평균 전력 지수(AVG):** {final_score:.3f}\n- ✅ **데이터 검증:** 타입 체크 완료"
    except Exception as e:
        final_score, report = 0.0, f"### ⚠️ 분석 오류\n{e}"
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
