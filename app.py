import streamlit as st
import pandas as pd
import datetime
import os
import numpy as np

# --- 1. 백엔드: 데이터 처리 및 분석 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path):
        return None
        
    df = pd.read_csv(file_path)
    
    # [누적 로직 1] 기본 팀 컬럼 생성
    if 'batter_team' not in df.columns:
        df['batter_team'] = np.where(df['inning_topbot'] == 'top', df['away_team'], df['home_team'])
        df['pitcher_team'] = np.where(df['inning_topbot'] == 'top', df['home_team'], df['away_team'])
    
    # [누적 로직 2] 선수별 주 소속팀(최빈값) 계산 및 매핑
    batter_map = df.groupby('batter')['batter_team'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    pitcher_map = df.groupby('pitcher')['pitcher_team'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    
    df['batter_2026_team'] = df['batter'].map(batter_map)
    df['pitcher_2026_team'] = df['pitcher'].map(pitcher_map)
    
    return df

@st.cache_data
def analyze_mlb_data(home, away):
    df = get_processed_data()
    if df is None: return None
    
    # 팀 매핑된 컬럼을 기준으로 경기 데이터 필터링
    match_data = df[(df['home_team'] == home) & (df['away_team'] == away)]
    
    if match_data.empty:
        return {"error": "해당 경기 데이터를 찾을 수 없습니다."}
    
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
    with st.spinner("데이터 처리 및 분석 중..."):
        result = analyze_mlb_data(home_team, away_team)
    
    if result and "error" not in result:
        st.subheader("📊 최종 분석 결과")
        col1, col2 = st.columns(2)
        col1.metric("평균 투구 구속", f"{result['avg_velocity']:.1f} mph")
        col2.metric("평균 타구 속도", f"{result['launch_speed']:.1f} mph")
    else:
        st.error("데이터 오류: 입력하신 팀명을 확인하거나 데이터 파일 상태를 점검하세요.")
