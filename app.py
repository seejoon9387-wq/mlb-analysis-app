import streamlit as st

st.title("⚾ MLB 승부 예측 분석기")
st.write("환영합니다! 이제 곧 우리만의 분석 시스템이 여기에 나타날 거예요.")

team1 = st.text_input("우리 팀(홈)", "Boston Red Sox")
team2 = st.text_input("상대 팀(원정)", "New York Yankees")

if st.button("분석 실행"):
    st.write(f"분석 중: {team1} vs {team2}")
    st.success("데이터 엔진을 곧 이곳에 연결할 예정입니다!")
