import streamlit as st

# 1. 통합 매핑 및 분석 엔진
MAPPING_TABLE = {
    "teams": {"보스턴": 111, "레드삭스": 111, "볼티모어": 110, "볼티": 110, "양키스": 147, "양키": 147},
    "players": {"디버스": "Rafael Devers", "저지": "Aaron Judge", "소토": "Juan Soto", "카사스": "Triston Casas"}
}

def find_exact_name(input_str, category="players"):
    source = MAPPING_TABLE.get(category, {})
    for key, val in source.items():
        if input_str in key: return val
    return input_str

def analyze_smart_lineup(team_name, lineup_list):
    team_id = find_exact_name(team_name, "teams")
    refined_lineup = [find_exact_name(p, "players") for p in lineup_list]
    
    # 분석 로직 (예시: 선수 수에 따른 가상 점수)
    power_score = len(refined_lineup) * 0.125
    return team_id, refined_lineup, power_score

# 2. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 지능형 라인업 분석기 v41.0")

col1, col2 = st.columns([1, 2])
team_input = col1.text_input("팀 입력", "보스턴")
lineup_input = col2.text_input("라인업 (콤마로 구분)", "디버스, 저지, 소토")

if st.button("분석 실행"):
    lineup_list = [p.strip() for p in lineup_input.split(',')]
    team_id, refined, score = analyze_smart_lineup(team_input, lineup_list)
    
    st.subheader(f"📊 {team_input} (ID: {team_id}) 분석 결과")
    st.write(f"정제된 라인업: **{', '.join(refined)}**")
    st.metric("최종 전력 점수", f"{score:.3f}")
    
    if score >= 0.3:
        st.success("강력한 타선이 감지되었습니다.")
