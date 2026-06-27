import streamlit as st
import requests
import pandas as pd
import time

# 1. 데이터 수집 함수 (웹 친화적)
@st.cache_data(ttl=3600) # 데이터를 1시간 동안 저장해두어 속도 향상
def get_mlb_data(year):
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={year}&startDate={year}-01-01&endDate={year}-12-31"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        games = []
        for date in data.get('dates', []):
            for game in date.get('games', []):
                if game['status']['abstractGameState'] == 'Final':
                    games.append({
                        'Date': date['date'],
                        'Away': game['teams']['away']['team']['name'],
                        'Home': game['teams']['home']['team']['name'],
                        'AwayScore': game['teams']['away'].get('score', 0),
                        'HomeScore': game['teams']['home'].get('score', 0)
                    })
        return pd.DataFrame(games)
    return pd.DataFrame()

# 2. 웹 화면
st.title("⚾ MLB 공식 데이터 분석기")

year_select = st.selectbox("연도를 선택하세요", [2024, 2025, 2026])

if st.button("데이터 불러오기"):
    with st.spinner(f"{year_select} 시즌 데이터를 수집 중입니다..."):
        df = get_mlb_data(year_select)
        if not df.empty:
            st.success(f"{len(df)}개의 경기 데이터를 찾았습니다!")
            st.dataframe(df.head(20)) # 상위 20개만 화면에 표시
            
            # CSV 다운로드 버튼
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("CSV로 다운로드", csv, f"mlb_data_{year_select}.csv", "text/csv")
        else:
            st.error("데이터를 가져오는 데 실패했습니다.")
