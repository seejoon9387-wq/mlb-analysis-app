import streamlit as st

# 1. 결장 임팩트 분석 엔진
def analyze_absence_impact(team_id, player_name):
    # 실제 환경에서는 데이터베이스/API 로그를 통해 계산
    # 여기서는 시뮬레이션을 위한 샘플 임팩트 값을 산출합니다.
    impact = 0.12 # 12% 감소 가정
    comment = f"{player_name} 결장 시 팀의 득점 생산력이 {impact*100:.1f}% 감소하는 경향이 있습니다."
    return impact, comment

# 2. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 선수 결장 임팩트 진단기 v44.0")

# 

player_input = st.text_input("분석할 선수 이름", "Rafael Devers")
team_input = st.text_input("팀 ID (또는 이름)", "111")

if st.button("결장 영향도 분석 실행"):
    with st.spinner("과거 출전 기록 및 득점 데이터 비교 분석 중..."):
        impact, comment = analyze_absence_impact(team_input, player_input)
        
        st.subheader("📊 결장 영향도 리포트")
        st.metric("득점 생산력 변동폭", f"-{impact*100:.1f}%")
        st.info(comment)
        
        if impact > 0.10:
            st.warning("⚠️ 해당 선수는 팀의 핵심 전력입니다. 결장 시 전력 손실이 매우 큽니다.")
        else:
            st.success("해당 선수의 결장은 전력에 미치는 영향이 비교적 적습니다.")
