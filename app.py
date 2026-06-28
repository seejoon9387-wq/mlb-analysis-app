import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

@st.cache_data
def get_master_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    # 데이터 내의 날짜 컬럼을 찾아서 datetime으로 변환 (사용자님 데이터의 날짜 컬럼명을 'date'로 통일)
    # 만약 컬럼명이 다르다면 알려주세요!
    df['date'] = pd.to_datetime(df.iloc[:, 0]) # 첫 번째 열이 날짜라고 가정
    return df

st.title("⚾ 시차 보정형 경기 기록 조회")
df = get_master_data()

selected_date = st.date_input("조회할 날짜 선택:", datetime(2026, 6, 29))

if st.button("데이터 조회 (시차 보정 포함)"):
    target = pd.Timestamp(selected_date)
    
    # 💡 [핵심] 선택한 날짜 당일 + 전날 데이터까지 모두 검색하여 매칭
    # 미국 시간과 한국 시간 차이로 인한 하루 오차 해결
    date_range = [target, target - timedelta(days=1)]
    result = df[df['date'].dt.date.isin([d.date() for d in date_range])]
    
    if not result.empty:
        st.success(f"{selected_date} 근접 데이터 발견 (시차 보정)")
        st.table(result)
    else:
        st.warning("선택한 날짜 및 전날에도 일치하는 데이터가 없습니다.")
