import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime, timedelta

FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"

@st.cache_data
def load_game_data(fid):
    url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
    try:
        res = requests.get(url)
        df = pd.read_csv(io.BytesIO(res.content))
        df.columns = [c.strip().lower() for c in df.columns]
        
        # 1. 날짜 데이터: 시간 제거 후 순수 날짜로 변환
        df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.normalize()
        
        # 2. 점수 데이터: 숫자로 강제 변환 (문자열 등 오염 제거)
        df['home_score'] = pd.to_numeric(df['home_score'], errors='coerce').fillna(0).astype(int)
        df['away_score'] = pd.to_numeric(df['away_score'], errors='coerce').fillna(0).astype(int)
        
        return df
    except Exception as e:
        return pd.DataFrame()

st.set_page_config(layout="wide")
st.title("⚾ MLB 2024-2026 경기 결과 (정밀 매칭)")

df = load_game_data(FILE_ID_GAME)

if not df.empty:
    selected_date = st.date_input("조회할 날짜를 선택하세요:", value=datetime.utcnow().date())
    
    # 3. 날짜 범위 검색 (±1일 범위 포함) - 시차 보정용
    target = pd.to_datetime(selected_date)
    match_data = df[(df['date'] >= target - timedelta(days=1)) & (df['date'] <= target + timedelta(days=1))]
    
    if not match_data.empty:
        # 데이터 시각화 시 점수 매칭 확인
        st.success(f"조회 결과 (전후 1일 포함): {len(match_data)}건의 기록")
        st.dataframe(match_data[['date', 'home_team', 'away_team', 'home_score', 'away_score', 'venue']], use_container_width=True)
    else:
        st.warning("해당 날짜 전후로 데이터를 찾을 수 없습니다.")
else:
    st.error("데이터 로드 실패")
