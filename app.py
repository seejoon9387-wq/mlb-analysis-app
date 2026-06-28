# 버전: v3.3
# 패치 내용: 선발 투수 정보 매칭 및 데이터 표시 강화
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import pytz

st.set_page_config(layout="wide", page_title="MLB AI 엔진 v3.3")
st.title("⚾ MLB AI 엔진 v3.3 (선발 투수 정보 포함)")

menu = st.sidebar.radio("메뉴", ["실시간 일정", "학습 데이터셋 관리"])

def get_mlb_schedule():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={today}&hydrate=probablePitcher"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        games = data['dates'][0]['games']
        schedule_list = []
        
        utc = pytz.utc
        kst = pytz.timezone('Asia/Seoul')
        
        for game in games:
            utc_dt = datetime.strptime(game['gameDate'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=utc)
            kst_dt = utc_dt.astimezone(kst)
            
            # 선발 투수 정보 가져오기 (없을 경우 '미정' 처리)
            home_pitcher = game['teams']['home'].get('probablePitcher', {}).get('fullName', '미정')
            away_pitcher = game['teams']['away'].get('probablePitcher', {}).get('fullName', '미정')
            
            schedule_list.append({
                "시간 (KST)": kst_dt.strftime('%H:%M'),
                "홈팀": game['teams']['home']['team']['name'],
                "원정팀": game['teams']['away']['team']['name'],
                "홈 선발": home_pitcher,
                "원정 선발": away_pitcher
            })
        return schedule_list
    except:
        return None

if menu == "실시간 일정":
    st.subheader(f"오늘 ({datetime.now().strftime('%Y-%m-%d')}) MLB 경기 및 선발 투수")
    with st.spinner('정보 로딩 중...'):
        games = get_mlb_schedule()
        if games:
            st.table(pd.DataFrame(games))
        else:
            st.error("데이터를 가져올 수 없거나 오늘 경기가 없습니다.")

elif menu == "학습 데이터셋 관리":
    # (v3.2 로직 유지)
    pass
