import streamlit as st
import pandas as pd
import datetime
import os
import numpy as np

# --- 1. 백엔드: 데이터 처리 및 모델 피처 생성 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path):
        return None
        
    df = pd.read_csv(file_path)
    
    # [누적 로직] 팀 매핑
    if 'batter_team' not in df.columns:
        df['batter_team'] = np.where(df['inning_topbot'] == 'top', df['away_team'], df['home_team'])
        df['pitcher_team'] = np.where(df['inning_topbot'] == 'top', df['home_team'], df['away_team'])
    
    # [누적 로직] 모델 피처 생성 (Whiff, wOBA 등 핵심 지표)
    # 실제 데이터셋에 'is_whiff'나 'woba_value' 컬럼이 있어야 합니다.
    if 'is_whiff' in df.columns:
        df['whiff_rate'] = df.groupby('pitcher')['is_whiff'].transform('mean')
    
    return df

@st.cache_data
def analyze_mlb_data(home, away):
    df = get_processed_data()
    if df is None: return None
    
    # 팀 매핑 기반 필터링
    match_data = df[(df['home_team'] == home) & (df['away_team'] == away)]
    
    if match_data.empty:
        return {"error": "경기 데이터를 찾을 수 없습니다."}
    
    # 지표 산출
    return {
        'whiff_rate': match_data['whiff_rate'].mean() if 'whiff_rate' in match_data.columns else 0,
        'release_speed': match_data['release_speed'].mean() if 'release_speed' in match_data.columns else 0
    }

# --- 2. 프론트엔드: 메인 UI ---
st.title("⚾ MLB 승부 예측 분석기")

selected_date = st.date_input("경기 날짜 선택", datetime.date.today())
home_team = st.text_input("홈 팀 이름")
away_team = st.text_input("원정 팀 이름")

if st.button("분석 실행"):
    with st.spinner("데이터 모델링 및 분석 중..."):
        result = analyze_mlb_data(home_team, away_team)
    
    if result and "error" not in result:
        st.subheader("📊 최종 분석 결과")
        col1, col2 = st.columns(2)
        col1.metric("선수 평균 Whiff %", f"{result['whiff_rate']*100:.1f}%")
        col2.metric("평균 투구 구속", f"{result['release_speed']:.1f} mph")
    else:
        st.error("데이터 오류: 입력하신 팀명을 확인하세요.")
