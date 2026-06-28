# 버전: v65.0
# 목적: 코랩 환경에서 pybaseball을 이용해 데이터가 정상적으로 저장되는지 검증
import streamlit as st
import pandas as pd
from pybaseball import statcast
import os

st.title("⚾ v65.0 데이터 생성 검증기")

if st.button("2024년 4월 데이터 수집 및 파일 저장"):
    with st.spinner("데이터를 수집 중입니다..."):
        try:
            # 테스트 수집
            df = statcast(start_dt="2024-04-01", end_dt="2024-04-07")
            save_path = "/content/mlb_test_2024.csv"
            df.to_csv(save_path, index=False)
            
            # 검증 단계
            if os.path.exists(save_path):
                st.success(f"성공! 파일이 생성되었습니다: {save_path}")
                st.write(f"데이터 크기: {df.shape}")
            else:
                st.error("파일 생성 실패: 경로를 확인하세요.")
        except Exception as e:
            st.error(f"오류 발생: {e}")

st.subheader("현재 /content 폴더 내 파일 목록")
st.write(os.listdir('/content/'))
