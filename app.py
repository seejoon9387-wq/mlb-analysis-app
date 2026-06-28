import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime
import pytz

st.set_page_config(layout="wide", page_title="MLB AI 엔진 v3.9.3")

# 데이터 로드 함수 (오류 진단 모드)
@st.cache_data
def fetch_master_data_debug():
    url_res = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY'
    url_stats = 'https://drive.google.com/uc?export=download&id=1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH'
    
    try:
        df_res = pd.read_csv(url_res)
        df_stats = pd.read_csv(url_stats)
        
        # 컬럼 확인용 출력
        st.write("### 데이터 구조 진단")
        st.write("df_res 컬럼:", df_res.columns.tolist())
        st.write("df_stats 컬럼:", df_stats.columns.tolist())
        
        return pd.merge(df_res, df_stats, on=['date', 'team'], how='inner')
    except Exception as e:
        st.error(f"상세 오류 내용: {e}")
        return None

menu = st.sidebar.radio("메뉴", ["데이터 구조 진단", "실시간 일정"])

if menu == "데이터 구조 진단":
    st.subheader("데이터 병합 컬럼 점검")
    if st.button("진단 시작"):
        master_df = fetch_master_data_debug()
        if master_df is not None:
            st.success("병합 성공!")
            st.write(master_df.head())
