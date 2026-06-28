import streamlit as st
import numpy as np

# 1. 커스텀 라인업 전력 산출 엔진
def get_player_stats(player_name):
    # 실제 환경에서는 선수 데이터베이스(CSV 등)에서 추출
    # 여기서는 예시를 위해 0.250~0.400 사이의 난수 가중치 적용
    np.random.seed(len(player_name)) 
    return np.random.uniform(0.250, 0.400)

def analyze_custom_lineup(team_name, custom_lineup):
    if not custom_lineup: return 0.0
    scores = [get_player_stats(p) for p in custom_lineup]
    return sum(scores) / len(scores)

# 2. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 커스텀 라인업 시뮬레이터 v39.0")

# 입력 파트
team_name = st.text_input("팀 이름", "보스턴 레드삭스")
lineup_input = st.text_area("예상 라인업 (선수 이름을 콤마로 구분)", "무키 베츠, 프레디 프리먼, 오타니 쇼헤이")

if st.button("라인업 전력 분석 실행"):
    lineup_list = [name.strip() for name in lineup_input.split(',')]
    
    with st.spinner("라인업 스탯 합산 및 전력 계산 중..."):
        score = analyze_custom_lineup(team_name, lineup_list)
        
        st.subheader(f"📊 {team_name} 분석 결과")
        st.metric("라인업 평균 전력 점수", f"{score:.3f}")
        
        # 
        
        if score > 0.350:
            st.success("매우 강력한 공격형 라인업입니다!")
        elif score > 0.300:
            st.info("리그 평균 수준의 안정적인 라인업입니다.")
        else:
            st.warning("타선의 보강이 필요한 라인업으로 보입니다.")

st.caption("Engine Status: Custom Lineup Analytics Active | v39.0")
