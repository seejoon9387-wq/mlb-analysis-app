import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

@st.cache_data
def get_master_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    return df

st.title("⚾ 데이터 날짜 자동 매칭 엔진")

df = get_master_data()

# 1. 사용자가 날짜 컬럼을 직접 선택하게 함 (에러 방지)
st.write("데이터의 컬럼 목록:", list(df.columns))
date_col = st.selectbox("날짜가 포함된 컬럼을 선택하세요:", df.columns)

# 2. 선택된 컬럼을 날짜 형식으로 변환
try:
    df['parsed_date'] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=['parsed_date']) # 날짜 변환 실패한 행 제거
    
    selected_date = st.date_input("조회할 날짜 선택:", datetime(2026, 6, 29))

    if st.button("결과 조회"):
        target = pd.Timestamp(selected_date)
        # 당일 + 전날 (시차 보정)
        res = df[df['parsed_date'].dt.date.isin([target.date(), (target - timedelta(days=1)).date()])]
        
        if not res.empty:
            st.table(res)
        else:
            st.warning("해당 날짜에 일치하는 데이터가 없습니다.")
except Exception as e:
    st.error(f"날짜 변환 중 오류: {e}. 선택한 컬럼이 정말 날짜인가요?")
