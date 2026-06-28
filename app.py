import streamlit as st
import pandas as pd
import statsapi
import os  # 여기서 os를 불러옵니다 (별도 설치 불필요)
from datetime import datetime

# --- [데이터 로드 함수: os 사용] ---
def check_and_load_data(file_path):
    # os.path.exists를 사용해 파일 존재 여부를 안전하게 확인
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return None

# --- [메인 엔진] ---
def main():
    st.title("⚾ MLB 최종 마스터 엔진 (v24.0)")
    
    menu = st.sidebar.selectbox("메뉴", ["실시간 경기 정보", "로컬 CSV 분석"])
    
    if menu == "실시간 경기 정보":
        if st.button("오늘 경기 불러오기"):
            # statsapi 호출
            today = datetime.now().strftime('%Y-%m-%d')
            data = statsapi.schedule(date=today)
            st.write(data)

    elif menu == "로컬 CSV 분석":
        file_path = 'full_mlb_events_2026.csv'
        df = check_and_load_data(file_path)
        if df is not None:
            st.dataframe(df)
        else:
            st.warning(f"파일을 찾을 수 없습니다: {file_path}")

if __name__ == "__main__":
    main()
