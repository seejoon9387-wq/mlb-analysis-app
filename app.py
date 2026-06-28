# 버전: v2.6
# 패치 내용: 구글 드라이브 파일 ID 직접 연동 및 데이터 통합 로직 자동화
import streamlit as st
import pandas as pd
import requests
import io

# 구글 드라이브 파일 ID 설정
RESULTS_FILE_ID = "1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY" # mlb_data_integrated.csv
STATS_FILE_ID = "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"    # final_data.csv

@st.cache_data
def load_drive_csv(file_id):
    """구글 드라이브에서 CSV를 읽어오는 함수"""
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return pd.read_csv(io.BytesIO(response.content))
    except Exception as e:
        st.error(f"데이터 로딩 중 오류 발생: {e}")
    return None

st.set_page_config(layout="wide", page_title="MLB AI 엔진 v2.6")
st.title("⚾ MLB AI 엔진 v2.6")

menu = st.sidebar.radio("메뉴", ["실시간 일정", "학습 데이터셋 관리"])

if menu == "학습 데이터셋 관리":
    st.subheader("클라우드 데이터 병합 센터")
    
    if st.button("데이터 병합 실행"):
        with st.spinner('구글 드라이브에서 데이터를 병합 중입니다...'):
            df_results = load_drive_csv(RESULTS_FILE_ID)
            df_stats = load_drive_csv(STATS_FILE_ID)
            
            if df_results is not None and df_stats is not None:
                # 병합 로직: 두 파일의 공통 컬럼(예: date, team)을 기준으로 병합
                # 만약 컬럼명이 다르다면 여기서 이름을 맞춰주는 작업이 필요합니다.
                master_df = pd.merge(df_results, df_stats, on=['date', 'team'], how='inner')
                
                st.success(f"성공! 통합 데이터셋 완성 (총 {len(master_df):,}행)")
                st.dataframe(master_df.head(), use_container_width=True)
            else:
                st.error("데이터 로드 실패: 구글 드라이브 공유 설정을 '링크가 있는 모든 사용자'로 변경했는지 확인하세요.")

elif menu == "실시간 일정":
    st.subheader("오늘의 MLB 경기 일정")
    st.info("실시간 API 엔진이 가동 중입니다.")
