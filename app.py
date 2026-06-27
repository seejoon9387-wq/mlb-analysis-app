import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt

# --- 1. 매핑 및 분석 엔진 ---
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
    source = MAPPING_TABLE.get(category, {})
    for key, val in source.items():
        if input_str in key: return val
    return input_str

def analyze_smart_lineup(team_name, lineup_list):
    # 팀 및 선수 이름 정제
    team_id = find_exact_name(team_name, "teams")
    refined_lineup = [find_exact_name(p.strip(), "players") for p in lineup_list]
    return team_id, refined_lineup

# --- 2. UI 및 메인 로직 ---
st.set_page_config(layout="wide")
st.title("⚾ 스마트 라인업 매치업 분석기")

# 설정
st.sidebar.header("경기 환경")
selected_date = st.sidebar.date_input("날짜", datetime.date(2026, 6, 28))
mode = st.radio("분석 방식", ["팀 단위", "라인업(선수) 단위"], horizontal=True)

# 입력
col1, col2 = st.columns(2)
if mode == "팀 단위":
    with col1: h_in = st.text_input("홈 팀")
    with col2: a_in = st.text_input("원정 팀")
else:
    with col1:
        h_lineup_raw = st.text_area("홈 라인업 (쉼표 구분)")
        h_pitcher = st.text_input("상대 선발 투수")
    with col2:
        a_lineup_raw = st.text_area("원정 라인업 (쉼표 구분)")
        a_pitcher = st.text_input("상대 선발 투수")

# 실행
if st.button("분석 실행"):
    if mode == "라인업(선수) 단위":
        # 스마트 분석 함수 호출
        h_team_id, h_refined = analyze_smart_lineup("홈 팀", h_lineup_raw.split(','))
        a_team_id, a_refined = analyze_smart_lineup("원정 팀", a_lineup_raw.split(','))
        
        st.write(f"🔍 **홈 라인업:** {h_refined}")
        st.write(f"🔍 **원정 라인업:** {a_refined}")
    
    st.success("데이터 정제 및 분석 완료!")
    
    
    # 예시 시각화
    fig, ax = plt.subplots()
    ax.bar(['홈 승리 확률', '원정 승리 확률'], [0.58, 0.42], color=['#FF4B4B', '#4B4BFF'])
    st.pyplot(fig)
