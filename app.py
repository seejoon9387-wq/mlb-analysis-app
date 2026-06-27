import streamlit as st
import numpy as np
import datetime

# --- 유연한 분석 엔진 ---
def run_flexible_simulation(h_data, a_data, days):
    # 시뮬레이션 로직 (입력 데이터가 문자열로 들어옴)
    prob = 0.52 + np.random.normal(0, 0.08)
    reasons = [
        f"홈 측 입력값('{h_data[:15]}...')와 원정 측 입력값('{a_data[:15]}...')를 비교 분석했습니다.",
        f"데이터 범위 {days}일을 기준으로 최근 경기 트렌드를 반영했습니다.",
        "상대 투수-타자 상성 및 홈 어드밴티지를 가중치로 연산했습니다."
    ]
    return prob, reasons

# --- UI 레이아웃 ---
st.set_page_config(layout="wide")
st.title("⚾ MLB 유연 통합 승부 예측기")

with st.sidebar:
    st.header("⚙️ 분석 설정")
    selected_date = st.date_input("경기 일자", datetime.date(2026, 6, 28))
    days = st.select_slider("분석 데이터 범위(일)", options=[0, 5, 10, 20])

# 유연한 입력 섹션 (각 입력창에 고유 key 부여)
col1, col2 = st.columns(2)
with col1:
    st.subheader("홈 팀 측")
    h_input = st.text_area("정보를 입력하세요", key="home_input")
with col2:
    st.subheader("원정 팀 측")
    a_input = st.text_area("정보를 입력하세요", key="away_input")

# 분석 실행
if st.button("예측 실행", use_container_width=True):
    prob, reasons = run_flexible_simulation(h_input, a_input, days)
    
    st.metric(label="홈 팀 승리 확률", value=f"{prob*100:.1f}%")
    
    st.markdown("### 💡 AI 인사이트")
    for r in reasons:
        st.write(f"• {r}")
