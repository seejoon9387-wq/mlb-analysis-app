import streamlit as st
import pandas as pd
from pybaseball import statcast
import os

# 각 연도별로 파일 분할 관리
def get_data_file_name(year):
    return f"mlb_data_{year}.csv"

def fetch_year_data(year):
    """특정 연도의 데이터를 가져와 파일로 저장합니다."""
    st.write(f"--- {year}년 데이터 수집 시작 (4월~10월) ---")
    all_months_data = []
    
    # 4월부터 10월까지 안전하게 반복
    for month in range(4, 11): 
        start = f"{year}-{month:02d}-01"
        # 월말 날짜를 안전하게 계산 (28일까지만 해도 충분)
        end = f"{year}-{month:02d}-28"
        try:
            data = statcast(start_dt=start, end_dt=end)
            all_months_data.append(data)
            st.write(f"  > {month}월 완료 ({len(data)}건)")
        except Exception as e:
            st.warning(f"  > {month}월 수집 중 오류 (건너뜁니다): {e}")
    
    if all_months_data:
        full_df = pd.concat(all_months_data)
        full_df.to_csv(get_data_file_name(year), index=False)
        return True
    return False

st.title("⚾ MLB 2024-2026 연도별 데이터 센터")

col1, col2, col3 = st.columns(3)
if col1.button("2024년 전체 수집"): fetch_year_data(2024)
if col2.button("2025년 전체 수집"): fetch_year_data(2025)
if col3.button("2026년 전체 수집"): fetch_year_data(2026)

st.subheader("데이터 파일 상태")
for y in [2024, 2025, 2026]:
    filename = get_data_file_name(y)
    if os.path.exists(filename):
        st.success(f"{y}년 데이터 파일 있음: {os.path.getsize(filename)/1024/1024:.1f} MB")
    else:
        st.warning(f"{y}년 데이터 파일 없음")
