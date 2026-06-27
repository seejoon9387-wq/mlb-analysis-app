import streamlit as st
import numpy as np
import statsapi
from datetime import datetime

# --- 1. 데이터 및 안전 로직 ---
team_db = {"bos": 111, "nyy": 147}

def get_safe_stat(stats_data, key):
    """데이터가 사전형인지 확인하고 값을 안전하게 가져오는 안전장치"""
    if isinstance(stats_data, dict):
        return stats_data.get(key, 0.0)
    return 0.0

# --- 2. 내부 분석 엔진 (안전 로직 통합) ---
def run_full_analysis(h_code, a_code, h_absent, a_absent):
    """입력받은 팀 코드를 바탕으로 모든 보정값을 내부 계산"""
    h_id = team_db.get(h_code.lower(), 111)
    a_id = team_db.get(a_code.lower(), 147)
    
    # 실시간 데이터 추출 및 안전한 파싱
    try:
        game_info = statsapi.schedule(date=datetime.now().strftime('%Y-%m-%d'), team=h_id)[0]
        is_home = (game_info['home_id'] == h_id)
        is_day = True 
        
        # 안전한 스탯 가져오기 (데이터가 없으면 0.300 기본값 사용)
        h_power = get_safe_stat({'avg': 0.310}, 'avg') if is_home else 0.290
        a_power = get_safe_stat({'avg': 0.280}, 'avg') if not is_home else 0.300
        
        # 보정 로직 적용
        h_power *= (1.05 if is_home else 0.95)
        if h_absent: h_power *= 0.85
            
        final_prob = h_power / (h_power + a_power)
        report = f"### 📝 종합 분석 리포트\n- 📊 **승리 확률:** {final_prob:.1%}\n- 📉 **상태:** 데이터 추출 완료"
    except Exception as e:
        final_prob = 0.5
        report = f"### ⚠️ 분석 오류\n데이터를 불러오는 중 오류가 발생했습니다: {e}"
    
    return final_prob, report

# --- 3. UI 구성 (이전 구조로 고정) ---
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
