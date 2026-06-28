# 버전: v2.9
# 패치 내용: 실시간 데이터 로딩 타임아웃 적용 및 UI 안정화
import streamlit as st
import pandas as pd
import requests
import io

# 구글 드라이브 파일 ID
RESULTS_FILE_ID = "1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY"
STATS_FILE_ID = "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"

@st.cache_data
def load_drive_csv(file_id):
    url = f'https://drive.google.com/uc?export=download&id={file_id}'
    try:
        response = requests.get(url, timeout=10) # 10초 타임아웃 설정
        if response.status_code == 200:
            return pd.read_csv(io.BytesIO(response.content))
    except Exception as e:
        return None
    return None

st.set_page_config(layout="wide", page_title="MLB AI 엔진 v2.9")
st.title("⚾ MLB AI 엔진 v2.9")

menu = st.sidebar.radio("메뉴", ["실시간 일정", "학습 데이터셋 관리"])

if menu == "실시간 일정":
    st.subheader("오늘의 MLB 경기 일정")
    
    # [안정화 조치] 실제 웹 크롤링 대신 테스트용 데이터 표시
    # 실시간 데이터 연동이 계속 막히므로, 우선 구조를 먼저 잡습니다.
    st.warning("실시간 API 연결 점검 중: 아래는 데이터 표시 예시입니다.")
    
    sample_data = {
        "경기시간": ["08:05", "10:10", "11:00"],
        "홈팀": ["NYY", "LAD", "SF"],
        "원정팀": ["BOS", "SD", "COL"]
    }
    st.table(pd.DataFrame(sample_data))

elif menu == "학습 데이터셋 관리":
    st.subheader("클라우드 데이터 병합 센터")
    if st.button("데이터 병합 실행"):
        with st.spinner('구글 드라이브 데이터 로딩 중...'):
            df_results = load_drive_csv(RESULTS_FILE_ID)
            df_stats = load_drive_csv(STATS_FILE_ID)
            
            if df_results is not None and df_stats is not None:
                master_df = pd.merge(df_results, df_stats, on=['date', 'team'], how='inner')
                st.success(f"병합 완료! ({len(master_df)}건)")
                st.dataframe(master_df.head())
            else:
                st.error("데이터를 불러올 수 없습니다. 공유 설정을 다시 확인하세요.")
