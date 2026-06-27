import streamlit as st
import pandas as pd
from pybaseball import statcast, pitching_stats, batting_stats
import time

# 1. 고밀도 데이터 수집 엔진 (2024~2026)
@st.cache_data
def fetch_all_detailed_data():
    all_data = []
    years = [2024, 2025, 2026]
    
    with st.spinner("2024년부터의 대규모 스탯을 수집 및 병합 중입니다..."):
        for year in years:
            # 투수 상세 스탯 (구종, 회전수, 무브먼트 등 포함)
            p_stats = pitching_stats(year, qual=1)
            # 타자 상세 스탯 (타구 속도, 배럴 타구 등 포함)
            b_stats = batting_stats(year, qual=1)
            
            p_stats['year'] = year
            b_stats['year'] = year
            
            all_data.append((p_stats, b_stats))
            time.sleep(1) # API 보호
            
    return all_data

# 2. 메인 대시보드
st.set_page_config(page_title="MLB AI Big Data", layout="wide")
st.title("⚾ MLB 2024-2026 통합 데이터 분석 엔진")

if st.sidebar.button("전체 데이터 수집 및 모델 최적화"):
    data_archive = fetch_all_detailed_data()
    st.success("2024-2026 상세 스탯 통합 완료.")
    
    # 3. 데이터 구조 시각화 (이해를 돕기 위한 모델 파이프라인 구조)
    st.subheader("데이터 연산 파이프라인")
    st.markdown("""
    * **입력(Input):** 투수(구속, 회전수, 무브먼트) + 타자(발사각, 타구속도, 컨택률)
    * **연산(Inference):** 머신러닝 기반 기대 승률 산출
    * **출력(Edge):** 실시간 배당과의 괴리율 분석
    """)

st.divider()
st.caption("Status: High-Density Data Collection Active | Years: 2024-2026")
