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
        
        # 1. 날짜 변환 및 한국 시간(KST) 적용
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        # UTC 데이터를 KST로 보정 (데이터가 UTC라면 +9시간)
        df['date'] = df['date'] + KST_OFFSET 
        
        return df
    except Exception as e:
        st.error(f"데이터 로드 에러: {e}")
        return pd.DataFrame()

# 페이지 설정
st.set_page_config(page_title="MLB KST 조회 시스템", layout="wide")
st.title("⚾ MLB 2024-2026 경기 결과 (KST 기준)")

# 데이터 로드
df = load_game_data(FILE_ID_GAME)

if not df.empty:
    # 한국 현재 날짜 계산
    today_kst = (datetime.utcnow() + KST_OFFSET).date()
    
    st.write(f"현재 한국 시간 기준 날짜: **{today_kst}**")
    
    # 🗓️ 달력 UI
    # 값 범위를 현재 날짜(오늘)로 자동 지정
    selected_date = st.date_input("조회할 날짜를 선택하세요:", value=today_kst)
    
    # 2. 날짜 필터링 (선택된 날짜의 KST 기준)
    match_data = df[df['date'].dt.date == selected_date]
    
    if not match_data.empty:
        st.success(f"{selected_date} 경기 결과 ({len(match_data)}건)")
        st.dataframe(match_data, use_container_width=True)
    else:
        st.warning(f"{selected_date}에 진행된 경기가 없습니다.")
else:
    st.error("데이터 로드에 실패했습니다. 파일 공유 설정을 다시 확인해주세요.")
