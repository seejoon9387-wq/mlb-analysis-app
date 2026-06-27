import streamlit as st
import statsapi

st.title("⚾ MLB 승부 예측 분석기")

# 팀 선택
team_name = st.selectbox("분석할 팀을 선택하세요", ["Boston Red Sox", "New York Yankees"])

if st.button("데이터 불러오기"):
    try:
        # 오늘 날짜로 데이터 가져오기
        schedule = statsapi.schedule(date='2026-06-28', team=team_name)
        if not schedule:
            st.warning("오늘 예정된 경기가 없습니다.")
        else:
            game_id = schedule[0]['game_id']
            st.success(f"데이터 연결 성공! (Game ID: {game_id})")
            st.write("이제 분석 엔진을 이식할 준비가 되었습니다.")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
