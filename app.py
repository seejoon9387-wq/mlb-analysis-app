import streamlit as st
import statsapi
import pandas as pd
import os

# 페이지 설정
st.set_page_config(page_title="MLB AI Analyst Pro", layout="wide")
st.title("⚾ MLB 정밀 분석 및 통합 시스템")

# 유틸리티 함수
@st.cache_data
def load_csv_data(file_name):
    file_path = os.path.join('/content/', file_name)
    return pd.read_csv(file_path)

def clean_team_name(input_name, available_teams):
    input_name = str(input_name).strip().lower()
    for team in available_teams:
        if input_name in team.lower():
            return team
    return input_name

# 사이드바 설정
mode = st.sidebar.radio("분석 모드 선택", ["공식 API 실시간 분석", "로컬 CSV 데이터 분석"])

# 분석 로직
if mode == "공식 API 실시간 분석":
    st.header("⚡ MLB Official Stats API")
    team_name = st.text_input("팀 이름 입력 (예: Dodgers, Yankees)")
    if st.button("실시간 팀 정보 조회"):
        try:
            team_info = statsapi.lookup_team(team_name)
            if team_info:
                st.json(team_info[0])
            else:
                st.error("팀 정보를 찾을 수 없습니다.")
        except Exception as e:
            st.error(f"API 호출 중 오류: {e}")

elif mode == "로컬 CSV 데이터 분석":
    st.header("📊 로컬 CSV 파일 정밀 분석")
    files = [f for f in os.listdir('/content/') if f.endswith('.csv')]
    selected_file = st.selectbox("파일 선택", files)
    
    if selected_file:
        df = load_csv_data(selected_file)
        col_list = df.columns.tolist()
        target_col = st.selectbox("기준 컬럼 선택 (팀/선수명)", col_list)
        search_query = st.text_input("검색어 입력 (자동 보정 적용)")
        
        if st.button("분석 엔진 가동"):
            unique_values = df[target_col].unique().tolist()
            corrected_query = clean_team_name(search_query, unique_values)
            result = df[df[target_col].astype(str).str.contains(corrected_query, case=False, na=False)]
            
            st.success(f"검색어 '{search_query}'를 '{corrected_query}'(으)로 보정하여 분석 완료!")
            st.dataframe(result, use_container_width=True)

st.divider()
st.caption("시스템 상태: 정상 | 경로: /content/ | 데이터베이스: 로컬 CSV + 공식 MLB API")
