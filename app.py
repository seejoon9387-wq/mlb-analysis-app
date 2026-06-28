import streamlit as st
import pandas as pd
from datetime import datetime

@st.cache_data
def get_master_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    
    # [핵심] 모든 컬럼을 순회하며 날짜 형식(YYYY-MM-DD 등)을 가진 컬럼을 찾음
    for col in df.columns:
        try:
            # 날짜로 변환 가능한지 테스트
            df['temp_date'] = pd.to_datetime(df[col])
            # 성공하면 해당 컬럼을 'date'로 확정
            df = df.rename(columns={col: 'date'})
            df['date'] = df['temp_date'].dt.strftime('%Y-%m-%d')
            break
        except:
            continue
    return df

st.title("⚾ CSV 날짜 기반 경기 기록 조회")
df = get_master_data()

# 데이터셋 내에 날짜 컬럼이 매칭되었는지 확인
if 'date' in df.columns:
    selected_date = st.date_input("조회할 날짜 선택 (2024~2026):", datetime(2026, 6, 29))
    
    if st.button("내 데이터에서 결과 조회"):
        target_date = selected_date.strftime('%Y-%m-%d')
        # 선택한 날짜에 맞는 행만 추출
        result = df[df['date'] == target_date]
        
        if not result.empty:
            st.success(f"{target_date}의 경기 기록")
            st.table(result)
        else:
            st.warning(f"{target_date}에 해당하는 데이터가 파일에 없습니다.")
else:
    st.error("데이터 파일 내에서 날짜 정보를 찾을 수 없습니다. CSV 파일에 날짜 컬럼이 있는지 확인해주세요.")
