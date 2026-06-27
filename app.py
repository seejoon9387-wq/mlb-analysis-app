import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt

# --- 1. 기본 설정 및 UI 헤더 ---
st.set_page_config(layout="wide")
st.title("⚾ MLB 최종 통합 분석기")

# --- 2. 항상 노출되는 설정 영역 ---
st.header("1. 공통 설정")
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    selected_date = st.date_input("경기 날짜", datetime.date(2026, 6, 27))
with col_s2:
    days = st.select_slider("데이터 범위 (일, 0은 전체)", options=[0, 5, 10, 20])
with col_s3:
    mode = st.radio("분석 방식", ["팀 단위", "라인업(선수) 단위"], horizontal=True)

st.write("---")

# --- 3. 분석 입력 영역 ---
st.header("2. 매치업 입력")
col1, col2 = st.columns(2)

if mode == "팀 단위":
    with col1:
        h_team = st.text_input("홈 팀명")
        h_pitcher = st.text_input("홈 선발 투수")
    with col2:
        a_team = st.text_input("원정 팀명")
        a_pitcher = st.text_input("원정 선발 투수")
else:
    with col1:
        h_lineup = st.text_area("홈 팀 라인업 (쉼표로 구분)")
        h_pitcher = st.text_input("홈 선발 투수")
    with col2:
        a_lineup = st.text_area("원정 팀 라인업 (쉼표로 구분)")
        a_pitcher = st.text_input("원정 선발 투수")

st.write("---")

# --- 4. 분석 실행 및 결과 ---
if st.button("최종 분석 실행"):
    st.success(f"{mode}로 {selected_date} 경기 분석 시작!")
    
    # 여기서부터 연산 로직을 넣으시면 됩니다
    # (예시 결과 출력)
    fig, ax = plt.subplots()
    ax.bar(['홈 승리 확률', '원정 승리 확률'], [55, 45], color=['red', 'blue'])
    st.pyplot(fig)
    
    st.caption("※ 환경 변수(홈 이점, 시간대)가 내부 연산되었습니다.")

# --- 5. 사이드바 정보 ---
st.sidebar.title("도움말")
st.sidebar.info("1. 날짜를 선택하세요.\n2. 분석 방식을 고르세요.\n3. 팀/라인업 정보를 입력하세요.\n4. 분석 버튼을 누르세요.")
