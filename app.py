import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime, timedelta

# 한국 시간대(KST) 설정
KST_OFFSET = timedelta(hours=9)
FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"

@st.cache_data
def load_game_data(fid):
    url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
    try:
        res = requests.get(url)
        df = pd.read_csv(io.BytesIO(res.content))
        df.columns = [c.strip().lower() for c in df.columns]
        
        # 1. 날짜 데이터 정제: 시간 정보(09:00:00)를 완전히 제거하고 날짜만 남김
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        # 한국 시간 보정 후 시간을 00:00:00으로 강제 초기화
        df['date'] = (df['date'] + KST_OFFSET).dt.normalize() 
        
        return df
    except Exception as e:
        st.error(f"데이터 로드 에러: {e}")
        return pd.DataFrame()

st.set_page_config(page_title="MLB 경기 조회", layout="wide")
st.title("⚾ MLB 2024-2026 경기 결과 조회")

df = load_game_data(FILE_ID_GAME)

if not df.empty:
    today_kst = (datetime.utcnow() + KST_OFFSET).date()
    
    # 달력 위젯 (이제 시간 정보 없이 날짜만 비교)
    selected_date = st.date_input("조회할 날짜를 선택하세요:", value=today_kst)
    selected_date_dt = pd.to_datetime(selected_date)
    
    # 2. 날짜 필터링 (시간 정보가 없는 날짜끼리 비교)
    match_data = df[df['date'] == selected_date_dt]
    
    if not match_data.empty:
        # 데이터프레임에서 날짜 컬럼을 보기 좋게 텍스트로 변환
        display_df = match_data.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        
        st.success(f"{selected_date} 경기 결과 ({len(match_data)}건)")
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning(f"{selected_date}에는 등록된 경기가 없습니다.")
else:
    st.error("데이터를 가져올 수 없습니다.")
