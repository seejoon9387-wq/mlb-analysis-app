# 버전: v65.0
import streamlit as st
import pandas as pd
from pybaseball import statcast
import os

st.title("⚾ v65.0 데이터 생성 검증기")

if st.button("2024년 4월 데이터 수집 테스트"):
    with st.spinner("수집 중..."):
        try:
            df = statcast(start_dt="2024-04-01", end_dt="2024-04-07")
            df.to_csv("/content/mlb_test_2024.csv", index=False)
            st.success("파일 저장 성공!")
        except Exception as e:
            st.error(f"오류: {e}")

st.write("현재 폴더 파일 목록:", os.listdir('/content/'))
