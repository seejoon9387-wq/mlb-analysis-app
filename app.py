# 버전: v2.8
# 패치 내용: NameError 수정 및 구조 안정화
import streamlit as st
import pandas as pd
import requests
import io

# 구글 드라이브 파일 ID (v2.6)
RESULTS_FILE_ID = "1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY"
STATS_FILE_ID = "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"

@st.cache_data
def load_drive_csv(file_id):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(io.BytesIO(response.content))
    return None

st.set_page_config(layout="wide", page_title="MLB AI 엔진 v2.8")
st.title("⚾ MLB AI 엔진 v2.8")

# 1. 사이드바 메뉴를 먼저 생성합니다.
menu = st.sidebar.radio("메뉴", ["실시간 일정", "학습 데이터셋 관리"])

# 2. 메뉴가 생성된 후에 값을 확인합니다.
if menu == "실시간 일정":
    st.subheader("오늘의 MLB 경기 일정")
    # v2.7에서 작동했던 크롤링 로직을 여기에 다시 배치
    st.info("실시간 경기 데이터 로딩 중...")
    # (여기에 이전 버전의 크롤링 코드 또는 API 호출 코드를 넣으세요)

elif menu == "학습 데이터셋 관리":
    st.subheader("클라우드 데이터 병합 센터")
    if st.button("데이터 병합 실행"):
        df_results = load_drive_csv(RESULTS_FILE_ID)
        df_stats = load_drive_csv(STATS_FILE_ID)
        
        if df_results is not None and df_stats is not None:
            master_df = pd.merge(df_results, df_stats, on=['date', 'team'], how='inner')
            st.success(f"데이터 병합 완료! 총 {len(master_df):,}행.")
            st.dataframe(master_df.head(), use_container_width=True)
        else:
            st.error("데이터 로드 실패.")
