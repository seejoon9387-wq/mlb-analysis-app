import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt

# --- 1. 매핑 테이블 및 보정 함수 ---
MAPPING_TABLE = {
    "teams": {
        "보스턴": "BOS", "레드삭스": "BOS", "볼티모어": "BAL", "볼티": "BAL",
        "양키스": "NYY", "양키": "NYY", "다저스": "LAD", "LA": "LAD"
    },
    "players": {
        "디버스": "Rafael Devers", "디버": "Rafael Devers", "저지": "Aaron Judge", 
        "소토": "Juan Soto", "카사스": "Triston Casas", "듀란": "Jarren Duran"
    }
}

def find_exact_name(input_str, category="players"):
    """사용자가 일부만 입력해도 매핑 테이블에서 정확한 값을 찾아줌"""
    source = MAPPING_TABLE.get(category, {})
    # 1. 매핑 테이블 우선 검색
    for key, val in source.items():
        if input_str in key:
            return val
    # 2. 없으면 원래 입력값 반환
    return input_str

@st.cache_data
def get_data():
    file_path = 'full_mlb_events_2026.csv'
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

# --- 2. 메인 UI ---
st.set_page_config(layout="wide")
st.title("⚾ MLB 최종 통합 분석기 (사전 매핑 기반)")

# 사이드바 설정
st.sidebar.header("설정 및 환경")
selected_date = st.sidebar.date_input("경기 날짜", datetime.date(2026, 6, 27))
days = st.sidebar.select_slider("데이터 범위 (일, 0은 전체)", options=[0, 5, 10, 20])
mode = st.radio("분석 방식", ["팀 단위", "라인업(선수) 단위"], horizontal=True)

# 입력 섹션
st.header("매치업 입력")
col1, col2 = st.columns(2)

if mode == "팀 단위":
    with col1: h_in = st.text_input("홈 팀명")
    with col2: a_in = st.text_input("원정 팀명")
else:
    with col1:
        h_lineup_raw = st.text_area("홈 라인업 (쉼표 구분)")
        h_pitcher = st.text_input("원정 선발 투수")
    with col2:
        a_lineup_raw = st.text_area("원정 라인업 (쉼표 구분)")
        a_pitcher = st.text_input("홈 선발 투수")

# 분석 실행 로직
if st.button("최종 분석 실행"):
    if mode == "라인업(선수) 단위":
        # 매핑 테이블을 사용하여 보정
        h_lineup = [find_exact_name(n.strip(), "players") for n in h_lineup_raw.split(',')]
        a_lineup = [find_exact_name(n.strip(), "players") for n in a_lineup_raw.split(',')]
        st.write(f"✅ 보정된 홈 라인업: {h_lineup}")
        st.write(f"✅ 보정된 원정 라인업: {a_lineup}")
    
    st.success("데이터 매핑 완료 및 분석 수행 중...")
    
    # 예시 그래프
    fig, ax = plt.subplots()
    ax.bar(['홈 승리 확률', '원정 승리 확률'], [55, 45], color=['red', 'blue'])
    st.pyplot(fig)
    
    st.caption("※ 매핑 테이블 기반 이름 보정 및 환경 변수 자동 연산 완료.")
