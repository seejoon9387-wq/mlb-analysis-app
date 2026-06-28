import streamlit as st

# 1. 낮/밤 환경 적응형 분석 엔진
def get_day_night_factor(player_id, is_hitting, is_day):
    # 실제 환경에서는 API 데이터를 활용하여 보정 계수를 동적으로 산출합니다.
    # 샘플 데이터: 낮 경기에 강한 타자 보정 적용
    return 1.15 if is_day else 0.95

def analyze_day_night_impact(lineup, starter_id, is_day):
    # 타선 보정
    lineup_scores = [0.300 * get_day_night_factor(p, True, is_day) for p in lineup]
    pitcher_factor = get_day_night_factor(starter_id, False, is_day)
    
    total_power = sum(lineup_scores) / len(lineup_scores)
    
    # 특이점 분석 코멘트
    comment = f"### 🕒 [시간대 상세 분석: {'낮' if is_day else '저녁'} 경기]\n"
    if pitcher_factor < 0.9:
        comment += "- **분석**: 선발 투수가 이 시간대에 매우 낮은 피안타율을 기록 중입니다.\n"
    elif pitcher_factor > 1.1:
        comment += "- **분석**: 선발 투수가 이 시간대에 다소 고전하는 경향이 있습니다.\n"
        
    return total_power / pitcher_factor, comment

# 2. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 환경 적응형 분석 엔진 v45.0")

# 

is_day = st.toggle("낮 경기 여부", value=True)

if st.button("시간대 환경 분석 실행"):
    with st.spinner("해당 시간대 선수별 성적 보정 중..."):
        score, comment = analyze_day_night_impact([1, 2, 3], 99, is_day)
        
        st.subheader("📊 환경 보정 리포트")
        st.metric("시간대 보정 후 전력 지수", f"{score:.3f}")
        st.markdown(comment)
        st.success("환경 적응형 분석 완료.")
