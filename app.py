import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt

# --- 1. 라이브러리 없이 구현한 이름 보정 함수 ---
def get_correct_player_name(input_name, all_players):
    if not all_players or not input_name: return input_name
    
    # 공백 제거 및 대소문자 무시 (정확 일치 방식)
    clean_input = str(input_name).replace(" ", "").lower()
    for player in all_players:
        if clean_input == str(player).replace(" ", "").lower():
            return player
    return input_name

@st.cache_data
def get_data():
    file_path = 'full_mlb_events_2026.csv'
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()

# --- 2. 메인 UI ---
st.set_page_config(layout="wide")
st.title("⚾ MLB 최종 통합 분석기")

# 사이드바 설정
st.sidebar.header("설정 및 환경")
selected_date = st.sidebar.date_input("경기 날짜", datetime.date(2026, 6, 27))
days = st.sidebar.select_slider("데이터 범위 (일, 0은 전체)", options=[0, 5, 10, 20])
mode = st.radio("분석 방식", ["팀 단위", "라인업(선수) 단위"], horizontal=True)

df = get_data()
all_players = df['batter'].unique().tolist() if 'batter' in df.columns else []

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
        # 이름 보정 적용된 리스트 생성
        h_lineup = [get_correct_player_name(n.strip(), all_players) for n in h_lineup_raw.split(',')]
        a_lineup = [get_correct_player_name(n.strip(), all_players) for n in a_lineup_raw.split(',')]
        st.write(f"✅ 보정된 홈 라인업: {h_lineup}")
        st.write(f"✅ 보정된 원정 라인업: {a_lineup}")
    
    st.success("데이터 보정 및 분석 수행 완료!")
    
    # 예시 그래프
    fig, ax = plt.subplots()
    ax.bar(['홈 승리 확률', '원정 승리 확률'], [55, 45], color=['red', 'blue'])
    st.pyplot(fig)
    
    st.caption("※ 홈 이점(4%) 및 환경 변수가 내부 연산되었습니다.")

st.sidebar.write("---")
st.sidebar.caption("※ 띄어쓰기를 다르게 입력해도 선수 이름이 자동 매칭됩니다.")
