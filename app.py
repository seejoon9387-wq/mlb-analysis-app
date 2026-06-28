# 버전: v3.8
# 패치 내용: 구글 드라이브 데이터 로드 및 실시간 경기 매칭 시스템
import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime
import pytz

# 1. 데이터 호출 및 병합 함수
@st.cache_data
def fetch_master_data():
    # 실제 병합 데이터셋 로드
    results_url = "https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY"
    stats_url = "https://drive.google.com/uc?export=download&id=1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"
    
    try:
        df_res = pd.read_csv(io.BytesIO(requests.get(results_url).content))
        df_stats = pd.read_csv(io.BytesIO(requests.get(stats_url).content))
        # 데이터 병합
        master = pd.merge(df_res, df_stats, on=['date', 'team'], how='inner')
        return master
    except: return None

# 2. 실시간 경기와 데이터 매칭 로직
def match_realtime_with_data(master_df):
    schedule = get_mlb_schedule() # 기존 함수 활용
    if master_df is None or schedule is None: return "데이터 로드 실패"
    
    # 오늘 경기 팀 추출
    match_report = []
    for game in schedule:
        home_team = game['홈팀']
        # master_df에 해당 팀의 데이터가 존재하는지 확인
        exists = home_team in master_df['team'].values
        match_report.append({"팀명": home_team, "데이터 매칭": "성공" if exists else "데이터 없음"})
    
    return pd.DataFrame(match_report)

# ... (기타 함수는 v3.7 유지)

if menu == "데이터 매칭 테스트":
    st.subheader("실제 데이터셋 매칭 엔진")
    if st.button("데이터 대입 매칭 시작"):
        with st.spinner('구글 드라이브 데이터와 실시간 경기 매칭 중...'):
            master_data = fetch_master_data()
            result_df = match_realtime_with_data(master_data)
            st.table(result_df)
