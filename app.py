# 버전: v3.2
# 패치 내용: UTC 시간을 한국 시간(KST)으로 변환 및 날짜 데이터 동기화
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

st.set_page_config(layout="wide", page_title="MLB AI 엔진 v3.2")
st.title("⚾ MLB AI 엔진 v3.2 (시간 보정 버전)")

menu = st.sidebar.radio("메뉴", ["실시간 일정", "학습 데이터셋 관리"])

def get_mlb_schedule():
    # 오늘 날짜 기반 API 호출
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={today}"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        games = data['dates'][0]['games']
        schedule_list = []
        
        # 시간대 설정 (UTC -> KST)
        utc = pytz.utc
        kst = pytz.timezone('Asia/Seoul')
        
        for game in games:
            # 원본 UTC 시간
            utc_dt = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=utc)
            # 한국 시간으로 변환
            kst_dt = utc_dt.astimezone(kst)
            
            schedule_list.append({
                "시간 (KST)": kst_dt.strftime('%H:%M'),
                "홈팀": game['teams']['home']['team']['name'],
                "원정팀": game['teams']['away']['team']['name']
            })
        return schedule_list
    except:
        return None

if menu == "실시간 일정":
    st.subheader(f"오늘 ({datetime.now().strftime('%Y-%m-%d')}) MLB 경기 일정")
    with st.spinner('한국 시간으로 변환 중...'):
        games = get_mlb_schedule()
        if games:
            st.table(pd.DataFrame(games))
        else:
            st.error("경기 데이터를 불러올 수 없습니다.")

elif menu == "학습 데이터셋 관리":
    # ... (기존 병합 로직 동일)
    pass
