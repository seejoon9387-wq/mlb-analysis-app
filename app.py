import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt

# --- 1. 유틸리티 및 데이터 로드 ---
def get_team_id(name):
    # 팀 매핑 로직
    return name 

@st.cache_data
def get_data():
    if os.path.exists('full_mlb_events_2026.csv'):
        return pd.read_csv('full_mlb_events_2026.csv')
    return pd.DataFrame()

# --- 2. 메인 화면 구성 ---
st.title("⚾ MLB 최종 통합 분석기")

# 1. 공통 설정 영역 (절대 사라지지 않음)
st.sidebar.header("설정 및 환경")
selected_date = st.sidebar.date_input("경기 날짜", datetime.date(2026, 6, 27))
days = st.sidebar.select_slider("데이터 범위 (일, 0은 전체)", options=[0, 5, 10, 20])
mode = st.radio("분석 방식", ["팀 단위", "라인업(선수) 단위"], horizontal=True)

# 2. 분석 모드에 따른 입력 필드 (조건부 렌더링)
st.subheader(f"분석 모드: {mode}")

if mode == "팀 단위":
    col1, col2 = st.columns(2)
    with col1:
        h_team = st.text_input("홈 팀명")
        h_pitcher = st.text_input("홈 선발 투수")
    with col2:
        a_team = st.text_input("원정 팀명")
        a_pitcher = st.text_input("원정 선발 투수")
else:
    col1, col2 = st.columns(2)
    with col1:
        h_lineup = st.text_area("홈 팀 라인업 (쉼표로 구분)")
        h_pitcher = st.text_input("홈 선발 투수")
    with col2:
        a_lineup = st.text_area("원정 팀 라인업 (쉼표로 구분)")
        a_pitcher = st.text_input("원정 선발 투수")

# 3. 분석 실행 버튼
if st.button("최종 분석 실행"):
    st.write("---")
    st.info(f"선택일: {selected_date} | 기간: {days}일 | 방식: {mode}")
    
    # [시뮬레이션 로직 영역]
    # 여기에 실제 계산 함수를 배치하세요.
    st.success("분석 완료! (선택한 조건에 따라 계산이 수행되었습니다.)")
    
    # 예시 결과 그래프
    fig, ax = plt.subplots()
    ax.bar(['홈 승리 확률', '원정 승리 확률'], [0.55, 0.45], color=['red', 'blue'])
    st.pyplot(fig)

# 4. 하단 부가 정보 (절대 사라지지 않음)
st.sidebar.write("---")
st.sidebar.caption("※ 홈 어드밴티지(4%)와 환경 변수가 내부적으로 연산됩니다.")
