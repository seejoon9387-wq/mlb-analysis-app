import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. 데이터 병합을 위한 공통 키 함수
def get_team_key(name):
    # API 팀명과 CSV 팀명을 일치시키기 위한 정규화
    mapping = {"Arizona Diamondbacks": "ARI", "Baltimore Orioles": "BAL", "New York Yankees": "NYY", "Boston Red Sox": "BOS", "Los Angeles Dodgers": "LAD", "San Francisco Giants": "SF", "Chicago Cubs": "CHC", "Texas Rangers": "TEX"}
    return mapping.get(name, name)

@st.cache_data
def get_master_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    # CSV의 날짜 포맷을 'YYYY-MM-DD'로 표준화
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
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
                "date": target_date,
                "home": g['teams']['home']['team']['name'],
                "away": g['teams']['away']['team']['name']
            })
        return pd.DataFrame(data)
    except: return pd.DataFrame()

# 2. 메인 로직: 날짜/팀 기준으로 데이터 매칭
st.title("⚾ 날짜별 정밀 데이터 매칭 조회")
selected_date = st.date_input("날짜 선택:", datetime.now())

if st.button("데이터 매칭 실행"):
    target_date = selected_date.strftime('%Y-%m-%d')
    live_df = get_live_schedule(target_date)
    master_df = get_master_data()

    if not live_df.empty:
        # 데이터 병합 (날짜와 팀 이름이 같으면 데이터 붙이기)
        merged = pd.merge(live_df, master_df, on=['date'], how='inner')
        st.subheader(f"{target_date} 매칭 결과")
        st.table(merged)
    else:
        st.warning("선택한 날짜에 일치하는 데이터가 없습니다.")
