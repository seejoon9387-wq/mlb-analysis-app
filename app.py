import streamlit as st
import pandas as pd

st.title("⚾ MLB 경기 결과 분석")

# 사용자가 파일을 직접 올리게 함
uploaded_file = st.file_uploader("mlb_final_master.csv 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = [c.strip().lower() for c in df.columns]
    df['date'] = df['date'].astype(str)
    
    # 달력 및 필터링
    selected_date = st.date_input("조회할 날짜를 선택하세요:")
    str_date = selected_date.strftime('%Y-%m-%d')
    
    match_data = df[df['date'] == str_date]
    
    if not match_data.empty:
        st.dataframe(match_data, use_container_width=True)
    else:
        st.warning(f"{str_date} 데이터가 없습니다.")
else:
    st.info("파일을 업로드하면 분석이 시작됩니다.")
