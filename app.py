import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime, timedelta

# KST 고정 함수
def get_kst_date(date_val):
    # 날짜를 읽어온 뒤 +9시간을 더해 KST로 고정
    dt = pd.to_datetime(date_val)
    return (dt + timedelta(hours=9)).normalize()

FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"

@st.cache_data
def load_game_data(fid):
    url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
    res = requests.get(url)
    df = pd.read_csv(io.BytesIO(res.content))
    df.columns = [c.strip().lower() for c in df.columns]
    
    # KST 강제 변환
    df['date'] = df['date'].apply(get_kst_date)
    
    # 점수 컬럼 강제 숫자화
    df['home_score'] = pd.to_numeric(df['home_score'], errors='coerce').fillna(0).astype(int)
    df['away_score'] = pd.to_numeric(df['away_score'], errors='coerce').fillna(0).astype(int)
    return df

st.set_page_config(layout="wide")
st.title("⚾ MLB 데이터 정밀 매칭 리포트")

df = load_game_data(FILE_ID_GAME)

# 달력
selected_date = st.date_input("조회할 날짜:", value=datetime.utcnow().date() + timedelta(hours=9))
target_date = pd.Timestamp(selected_date).normalize()

# 매칭 확인
match_data = df[df['date'] == target_date]

if not match_data.empty:
    st.success(f"{selected_date} 경기: {len(match_data)}건")
    st.dataframe(match_data, use_container_width=True)
    
    # 🔍 데이터가 꼬였는지 확인하는 디버깅 테이블
    st.write("---")
    st.write("### 데이터 구조 체크 (이름과 점수가 맞는지 확인하세요)")
    st.table(match_data[['home_team', 'home_score', 'away_team', 'away_score']].head(10))
else:
    st.warning("데이터 없음. 데이터 원본의 날짜 형식을 확인하세요.")
