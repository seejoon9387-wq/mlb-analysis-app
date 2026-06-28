import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime, timedelta

FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"

@st.cache_data
def load_game_data(fid):
    url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
    res = requests.get(url)
    df = pd.read_csv(io.BytesIO(res.content))
    df.columns = [c.strip().lower() for c in df.columns]
    
    # 1. 날짜 형식을 순수 날짜로 변환 (시간 정보 제거)
    # format='mixed'를 사용하여 다양한 날짜 형식을 수용합니다.
    df['date'] = pd.to_datetime(df['date'], errors='coerce', format='mixed').dt.date
    
    return df

st.set_page_config(layout="wide")
st.title("⚾ MLB 최종 경기 결과 조회")

df = load_game_data(FILE_ID_GAME)

# 오늘 날짜 (한국 시간 기준)
today_kst = datetime.utcnow().date() + timedelta(hours=9)

# 🗓️ 달력 위젯
selected_date = st.date_input("조회할 날짜를 선택하세요:", value=today_kst)

# 2. 날짜 데이터 비교 (시간 정보가 없는 순수 날짜끼리 비교)
match_data = df[df['date'] == selected_date]

if not match_data.empty:
    st.success(f"{selected_date} 경기 결과 ({len(match_data)}건)")
    # 점수와 팀 정보를 명확하게 표시
    st.dataframe(match_data[['date', 'home_team', 'home_score', 'away_team', 'away_score', 'venue', 'attendance']], 
                 use_container_width=True)
else:
    st.warning(f"{selected_date}에 해당하는 경기 데이터가 없습니다.")
    st.write("데이터의 날짜 확인:", df['date'].unique()) # 디버깅용: 데이터에 들어있는 날짜들 확인
