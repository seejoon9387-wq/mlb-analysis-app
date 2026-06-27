import streamlit as st
import pandas as pd
import datetime
import os
import numpy as np

# --- 1. 백엔드: 데이터 정제 및 처리 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path):
        return None
    
    df = pd.read_csv(file_path)
    
    # [누적 로직] 1. 팀 매핑 및 공식 데이터 확정
    if 'batter_team' not in df.columns:
        df['batter_team'] = np.where(df['inning_topbot'] == 'top', df['away_team'], df['home_team'])
        df['pitcher_team'] = np.where(df['inning_topbot'] == 'top', df['home_team'], df['away_team'])
    
    # 선수별 주 소속팀 매핑
    batter_map = df.groupby('batter')['batter_team'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    pitcher_map = df.groupby('pitcher')['pitcher_team'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    
    df['batter_2026_team'] = df['batter'].map(batter_map)
    df['pitcher_2026_team'] = df['pitcher'].map(pitcher_map)
    
    # [누적 로직] 2. 데이터 정제 (결측치 채우기)
    df['pitcher_team_official'] = df.get('pitcher_team_official', pd.Series(dtype=object)).fillna(df['pitcher_2026_team'])
    df['batter_team_official'] = df.get('batter_team_official', pd.Series(dtype=object)).fillna(df['batter_2026_team'])
    
    cols_to_fill = ['launch_speed', 'is_whiff', 'release_speed']
    for col in cols_to_fill:
        if col in df.columns:
            df[col] = df[col].fillna(0)
            
    return df

@st.cache_data
def analyze_mlb_data(home, away):
    df = get_processed_data()
    if df is None: return {"error": "데이터 파일 없음"}
    
    match_data = df[(df['home_team'] == home) & (df['away_team'] == away)]
    
    if match_data.empty:
        return {"error": "해당 경기 데이터가 없습니다."}
    
    return {
        'avg_velocity': match_data['release_speed'].mean(),
        'avg_launch_speed': match_data['launch_speed'].mean()
    }

# --- 2. 프론트엔드: 메인 UI ---
st.title("⚾ MLB 승부 예측 분석기")

selected_date = st.date_input("경기 날짜 선택", datetime.date.today())
home_team = st.text_input("홈 팀 이름")
away_team = st.text_input("원정 팀 이름")

if st.button("분석 실행"):
    with st.spinner("데이터 정제 및 분석 중..."):
        result = analyze_mlb_data(home_team, away_team)
    
    if result and "error" not in result:
        st.subheader("📊 최종 분석 결과")
        col1, col2 = st.columns(2)
        col1.metric("평균 투구 구속", f"{result['avg_velocity']:.1f} mph")
        col2.metric("평균 타구 속도", f"{result['avg_launch_speed']:.1f} mph")
    else:
        st.error(result.get("error", "데이터 오류"))
