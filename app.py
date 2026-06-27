import streamlit as st
import pandas as pd
import datetime
import os
import numpy as np

# --- 1. 백엔드: 데이터 처리 및 검증 엔진 ---
@st.cache_data
def get_processed_data():
    file_path = 'full_mlb_events_2026.csv'
    if not os.path.exists(file_path):
        return None
    
    df = pd.read_csv(file_path)
    
    # [누적 로직] 팀 매핑 및 피처 생성
    if 'batter_team' not in df.columns:
        df['batter_team'] = np.where(df['inning_topbot'] == 'top', df['away_team'], df['home_team'])
        df['pitcher_team'] = np.where(df['inning_topbot'] == 'top', df['home_team'], df['away_team'])
    
    # [누적 로직] 데이터 누락 확인 (디버깅용)
    missing_report = df.isnull().sum()
    missing_report = missing_report[missing_report > 0]
    
    return df, missing_report

@st.cache_data
def analyze_mlb_data(home, away):
    df, missing_report = get_processed_data()
    if df is None: return {"error": "파일 없음"}
    
    match_data = df[(df['home_team'] == home) & (df['away_team'] == away)]
    
    if match_data.empty:
        return {"error": "해당 경기 데이터가 없습니다."}
    
    return {
        'avg_velocity': match_data['release_speed'].mean() if 'release_speed' in match_data.columns else 0,
        'missing': missing_report,
        'sample': df.head(1).to_dict(orient='records')
    }

# --- 2. 프론트엔드: 메인 UI ---
st.title("⚾ MLB 승부 예측 분석기")

selected_date = st.date_input("경기 날짜 선택", datetime.date.today())
home_team = st.text_input("홈 팀 이름")
away_team = st.text_input("원정 팀 이름")

if st.button("분석 실행"):
    with st.spinner("데이터 검증 및 분석 중..."):
        result = analyze_mlb_data(home_team, away_team)
    
    if result and "error" not in result:
        st.subheader("📊 최종 분석 결과")
        st.metric("평균 투구 구속", f"{result['avg_velocity']:.1f} mph")
        
        # 디버깅용: 데이터 상태 확인 (관리자용)
        with st.expander("데이터 검증 리포트 (관리자)"):
            st.write("누락 데이터:", result['missing'] if not result['missing'].empty else "없음 (정상)")
            st.write("최신 샘플:", result['sample'])
    else:
        st.error(result.get("error", "데이터 오류"))
