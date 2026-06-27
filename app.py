import streamlit as st
import pandas as pd
import datetime
import os
import numpy as np

# --- 1. 백엔드: 데이터 분석, 팀 매핑 및 결손 체크 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path):
        return None
        
    df = pd.read_csv(file_path)
    
    # [누적 로직] 팀 매핑 및 공식 데이터 확정
    if 'batter_team' not in df.columns:
        df['pitcher_team'] = np.where(df['inning_topbot'] == 'top', df['away_team'], df['home_team'])
        df['batter_team'] = np.where(df['inning_topbot'] == 'top', df['home_team'], df['away_team'])
    
    # [누적 로직] 선수별 소속 팀 공식 매핑 (가장 빈도 높은 팀으로 확정)
    team_map = df.groupby('batter')['batter_team'].agg(lambda x: x.mode()[0] if not x.mode().empty else "Unknown").to_dict()
    df['batter_team_official'] = df['batter'].map(team_map)
    
    return df

@st.cache_data
def analyze_mlb_data(home, away):
    df = get_processed_data()
    if df is None: return None
    
    # 데이터 필터링
    match_data = df[(df['home_team'] == home) & (df['away_team'] == away)]
    
    if match_data.empty:
        return {"error": "경기 데이터를 찾을 수 없습니다."}
    
    return {
        'avg_velocity': match_data['release_speed'].mean() if 'release_speed' in match_data.columns else 0,
        'launch_speed': match_data['launch_speed'].mean() if 'launch_speed' in match_data.columns else 0
    }

# --- 2. 프론트엔드: 메인 UI ---
st.title("⚾ MLB 승부 예측 분석기")

selected_date = st.date_input("경기 날짜 선택", datetime.date.today())
home_team = st.text_input("홈 팀 이름 (예: NYY)")
away_team = st.text_input("원정 팀 이름 (예: BOS)")

if st.button("분석 실행"):
    with st.spinner("데이터 매핑 및 분석 중..."):
        result = analyze_mlb_data(home_team, away_team)
    
    if result and "error" not in result:
        st.subheader("📊 최종 분석 결과")
        col1, col2 = st.columns(2)
        col1.metric("평균 투구 구속", f"{result['avg_velocity']:.1f} mph")
        col2.metric("평균 타구 속도", f"{result['launch_speed']:.1f} mph")
    else:
        st.error("데이터 오류 발생 (입력하신 팀명을 확인하세요)")
