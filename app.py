# 버전: v3.1
# 패치 내용: MLB 공식 API를 사용하여 실시간 일정 로딩 구현
import streamlit as st
import requests

def get_realtime_mlb_schedule():
    # MLB 공식 실시간 일정 API (무료)
    url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # 경기 데이터 추출 (단순화)
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

# 메뉴 안에 삽입
if menu == "실시간 일정":
    st.subheader("오늘의 MLB 경기 일정")
    with st.spinner('실시간 API에서 데이터를 가져오는 중...'):
        games = get_realtime_mlb_schedule()
        if games:
            st.table(games)
        else:
            st.error("데이터를 가져올 수 없습니다.")
