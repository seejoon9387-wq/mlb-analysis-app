# 버전: v72.0
# 목적: 메모리 오류 방지를 위한 월별 개별 수집 및 즉시 다운로드
import streamlit as st
import pandas as pd
from pybaseball import statcast

st.title("⚾ v72.0 메모리 안전 수집기")

year = st.selectbox("연도 선택", [2024, 2025, 2026])
month = st.selectbox("수집할 월 선택", range(3, 10))

if st.button(f"{year}년 {month}월 데이터 수집"):
    try:
        with st.spinner(f"{year}년 {month}월 수집 중..."):
            start = f"{year}-{month:02d}-01"
            end = f"{year}-{month:02d}-28"
            
            data = statcast(start_dt=start, end_dt=end)
            
            st.success(f"{len(data)}건 수집 완료!")
            
            # 여기서 바로 다운로드 버튼 제공 (메모리에 안 쌓음)
            csv = data.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"{year}_{month}월 데이터 다운로드",
                data=csv,
                file_name=f"mlb_{year}_{month}.csv",
                mime='text/csv'
            )
    except Exception as e:
        st.error(f"오류: {e}")
