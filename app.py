import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    # 현재 스크립트 파일(app.py)이 있는 위치를 기준으로 경로 설정
    file_path = os.path.join(os.path.dirname(__file__), "mlb_final_master.csv")
    
    # 파일이 존재하는지 확인
    if not os.path.exists(file_path):
        st.error(f"파일을 찾을 수 없습니다: {file_path}")
        return pd.DataFrame() # 빈 데이터프레임 반환
        
    df = pd.read_csv(file_path)
    df.columns = [c.strip().lower() for c in df.columns]
    df['date'] = df['date'].astype(str)
    return df

st.title("⚾ MLB 경기 결과 분석")
df = load_data()

if not df.empty:
    st.dataframe(df.head())
else:
    st.write("데이터가 로드되지 않았습니다.")
