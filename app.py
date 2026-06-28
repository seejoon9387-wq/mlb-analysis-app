import streamlit as st
import pandas as pd
from pybaseball import statcast
import os

DATA_FILE = "all_mlb_teams_data.csv"

# 팀 목록 (30개 팀 확인용)
MLB_TEAMS = ['LAA', 'HOU', 'OAK', 'SEA', 'TEX', 'ATL', 'MIA', 'NYM', 'PHI', 'WSN', 
             'CHC', 'MIL', 'STL', 'PIT', 'CIN', 'LAD', 'COL', 'SD', 'SF', 'ARI', 
             'BAL', 'BOS', 'NYY', 'TB', 'TOR', 'CLE', 'DET', 'KC', 'MIN', 'CWS']

def fetch_full_mlb_data():
    """2024~2026 전체 팀 데이터를 수집합니다."""
    years = [2024, 2025, 2026]
    all_years_data = []
    
    for year in years:
        st.write(f"--- {year}년 전체 데이터 수집 시작 ---")
        # 한 번에 너무 많은 데이터를 요청하면 차단될 수 있으므로 분할 호출
        # 예: 3개월 단위로 나누어 호출
        for month in range(4, 10):  # 4월~9월 시즌 중
            start = f"{year}-{month:02d}-01"
            end = f"{year}-{month:02d}-28"
            try:
                monthly_data = statcast(start_dt=start, end_dt=end)
                all_years_data.append(monthly_data)
                st.write(f"{year}년 {month}월 완료 ({len(monthly_data)}건)")
            except Exception as e:
                st.error(f"{year}년 {month}월 데이터 호출 실패: {e}")
                
    if all_years_data:
        full_df = pd.concat(all_years_data)
        full_df.to_csv(DATA_FILE, index=False)
        return full_df
    return pd.DataFrame()

st.title("⚾ MLB 30개 팀 통합 데이터 센터")

if st.button("전체 팀 데이터 (2024-2026) 재수집"):
    df = fetch_full_mlb_data()
    if not df.empty:
        st.success("30개 팀 전체 데이터 수집 및 저장 완료!")
        st.rerun()

# 데이터 로딩 및 팀별 분석
if os.path.exists(DATA_FILE):
    st.info("데이터가 준비되었습니다. 팀을 선택하여 분석하세요.")
    df = pd.read_csv(DATA_FILE)
    selected_team = st.selectbox("분석할 팀 선택", sorted(df['home_team'].unique()))
    
    team_data = df[df['home_team'] == selected_team]
    st.write(f"선택하신 {selected_team}팀의 데이터 규모: {len(team_data)}건")
    st.table(team_data.head(5))
