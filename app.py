import streamlit as st
import pandas as pd
import requests
from datetime import datetime

@st.cache_data
def get_master_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    # 컬럼 이름 확인 (away_team, away_score, home_team, home_score)
    return df

@st.cache_data
def get_live_schedule(target_date):
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={target_date}&hydrate=linescore"
    try:
        response = requests.get(url).json()
        games = response['dates'][0]['games']
        data = []
        for g in games:
            data.append({
                "홈팀": g['teams']['home']['team']['name'],
                "원정팀": g['teams']['away']['team']['name']
            })
        return pd.DataFrame(data)
    except: return pd.DataFrame()

# 메인 로직
st.title("⚾ 팀 간 상대 전적 분석기")

if st.button("분석 실행"):
    master_df = get_master_data()
    live_df = get_live_schedule(datetime.now().strftime('%Y-%m-%d'))
    
    if not live_df.empty:
        results = []
        for _, row in live_df.iterrows():
            h, a = row['홈팀'], row['원정팀']
            # CSV에서 홈팀/원정팀이 일치하는 기록 필터링
            match = master_df[(master_df['home_team'] == h) & (master_df['away_team'] == a)]
            
            if not match.empty:
                avg_h = match['home_score'].mean()
                avg_a = match['away_score'].mean()
                results.append({"홈팀": h, "원정팀": a, "평균 득점(홈)": round(avg_h, 1), "평균 득점(원정)": round(avg_a, 1)})
            else:
                results.append({"홈팀": h, "원정팀": a, "평균 득점(홈)": "기록없음", "평균 득점(원정)": "기록없음"})
        
        st.table(pd.DataFrame(results))
    else:
        st.warning("실시간 경기 데이터를 가져올 수 없습니다.")
