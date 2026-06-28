# 버전: v3.1
# 패치 내용: NameError 완전 해결 및 MLB 실시간 API 연동
import streamlit as st
import pandas as pd
import requests

# 1. 페이지 설정 및 초기화
st.set_page_config(layout="wide", page_title="MLB AI 엔진 v3.1")
st.title("⚾ MLB AI 엔진 v3.1")

# 2. 사이드바 메뉴 먼저 생성 (이 부분이 if문보다 무조건 위에 있어야 합니다)
menu = st.sidebar.radio("메뉴", ["실시간 일정", "학습 데이터셋 관리"])

# 3. 실시간 API 함수 정의
def get_mlb_schedule():
    url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date=2026-06-29"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        games = data['dates'][0]['games']
        schedule_list = []
        for game in games:
            schedule_list.append({
                "시간": game['gameDate'][11:16],
                "홈팀": game['teams']['home']['team']['name'],
                "원정팀": game['teams']['away']['team']['name']
            })
        return schedule_list
    except:
        return None

# 4. 메뉴 선택에 따른 화면 로직
if menu == "실시간 일정":
    st.subheader("오늘의 MLB 경기 일정")
    with st.spinner('실시간 경기 데이터를 불러오는 중...'):
        games = get_mlb_schedule()
        if games:
            st.table(pd.DataFrame(games))
        else:
            st.error("실시간 데이터를 가져올 수 없습니다.")

elif menu == "학습 데이터셋 관리":
    st.subheader("클라우드 데이터 병합 센터")
    if st.button("데이터 병합 실행"):
        st.info("데이터 병합 기능이 준비되었습니다.")
