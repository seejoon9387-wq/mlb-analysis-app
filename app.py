import streamlit as st
import numpy as np
import statsapi
import json
from datetime import datetime

# --- 1. 데이터 디버깅 및 안전 파싱 ---
def inspect_environment():
    """현재 네임스페이스 내 가용한 변수와 데이터 상태를 검증"""
    available_vars = dir()
    print("--- 현재 저장된 변수 목록 ---")
    print([v for v in available_vars if not v.startswith('_')])
    return available_vars

def parse_and_validate(data_var):
    """지정된 변수의 타입과 내용을 안전하게 출력하는 검증기"""
    print(f"데이터 타입: {type(data_var)}")
    print(f"데이터 내용: {data_var}")
    return isinstance(data_var, (dict, list, str))

# --- 2. 분석 엔진 (디버깅 루틴 통합) ---
def run_full_analysis(h_code, a_code):
    try:
        # 데이터 수집 전 환경 확인
        inspect_environment()
        
        # 실제 데이터 수집
        h_id = 111 
        stats = statsapi.player_stats(h_id, group='hitting', type='season')
        
        # 검증 루틴 적용
        parse_and_validate(stats)
        
        report = "### 📝 시스템 디버깅 완료\n데이터 구조 확인 및 분석 준비 완료."
    except Exception as e:
        report = f"### ⚠️ 디버깅 오류\n{e}"
    return report

# --- 3. UI 구성 (고정) ---
st.set_page_config(page_title="MLB AI Analyst", layout="centered")
st.title("⚾ MLB AI 분석 시스템")

col_top1, col_top2 = st.columns(2)
target_date = col_top1.date_input("분석 날짜", datetime.now())
days_range = col_top2.slider("분석 범위 (최근 N일)", 1, 30, 7)

tab1, tab2 = st.tabs(["⚡ 자동 실시간 분석", "🔍 수동 정밀 분석"])

with tab1:
    h_code = st.text_input("홈 팀 코드", key="h_auto")
    if st.button("분석 실행 (자동)"):
        report = run_full_analysis(h_code, "")
        st.write(report)

with tab2:
    st.info("수동 분석 모드입니다.")
    if st.button("데이터 상태 검사"):
        inspect_environment()
        st.success("콘솔에서 변수 목록을 확인하세요.")
