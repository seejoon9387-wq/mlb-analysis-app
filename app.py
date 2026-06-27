import streamlit as st
import numpy as np

# --- 분석 로직 (모드별 분기) ---
def run_analysis(h_input, a_input, days, mode):
    # 모드에 따른 시뮬레이션 가중치 변경 로직
    prob = 0.55 if mode == "팀 분석" else 0.58
    prob += np.random.normal(0, 0.02)
    
    comment = f"[{mode}] 모드로 {days}일간의 데이터를 분석했습니다."
    return prob, comment

# --- UI 레이아웃 ---
st.set_page_config(layout="wide")
st.title("⚾ MLB 통합 승부 예측 시스템")

# 1. 상단 모드 선택 탭
tab1, tab2 = st.tabs(["📊 팀 단위 분석", "👤 라인업 정밀 분석"])

with st.sidebar:
    days = st.select_slider("데이터 분석 범위(일)", options=[0, 5, 10, 20, 30])

# 2. 탭별 입력 처리
with tab1:
    st.info("팀명만 입력하세요. (예: 양키스, 다저스)")
    col1, col2 = st.columns(2)
    with col1: h_team = st.text_input("홈 팀명", key="h_team")
    with col2: a_team = st.text_input("원정 팀명", key="a_team")
    mode = "팀 분석"
    h_in, a_in = h_team, a_team

with tab2:
    st.info("라인업을 쉼표로 구분하여 입력하세요.")
    col1, col2 = st.columns(2)
    with col1: h_lineup = st.text_area("홈 라인업", key="h_lineup")
    with col2: a_lineup = st.text_area("원정 라인업", key="a_lineup")
    mode = "라인업 분석"
    h_in, a_in = h_lineup, a_lineup

# 3. 분석 실행 (공통)
if st.button("최종 분석 실행", use_container_width=True):
    prob, comment = run_analysis(h_in, a_in, days, mode)
    st.divider()
    st.metric("승리 확률", f"{prob*100:.1f}%")
    st.write(f"💡 **근거:** {comment}")
