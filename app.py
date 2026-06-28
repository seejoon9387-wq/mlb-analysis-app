import streamlit as st
import statsapi

# 1. 지능형 팀 ID 매핑 함수
def get_team_id_by_name(input_name):
    team_db = {
        '볼티': 110, '볼티모어': 110, '오리올스': 110,
        '양키스': 147, '뉴욕': 147, '양키': 147,
        '보스턴': 111, '레드삭스': 111, '보삭': 111,
        '다저스': 119, 'LA': 119
    }
    for key, team_id in team_db.items():
        if input_name in key:
            return team_id
    return None

# 2. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 지능형 매치업 분석기 v38.0")

# 사용자 입력단
col1, col2 = st.columns(2)
home_input = col1.text_input("홈 팀 입력 (예: 볼티)", "보스턴")
away_input = col2.text_input("원정 팀 입력 (예: 양키)", "양키스")

if st.button("분석 실행"):
    home_id = get_team_id_by_name(home_input)
    away_id = get_team_id_by_name(away_input)
    
    if home_id and away_id:
        with st.spinner("라이브 데이터를 불러오는 중..."):
            # 라인업 호출 (v37.0 로직)
            st.success(f"분석 시작: 홈 ID({home_id}) vs 원정 ID({away_id})")
            
            # [여기에 get_lineup_live_safe 호출 및 시각화 로직 삽입]
            st.write("라인업 데이터 분석을 수행합니다...")
    else:
        st.error("팀 정보를 찾을 수 없습니다. 다시 입력해 주세요.")
