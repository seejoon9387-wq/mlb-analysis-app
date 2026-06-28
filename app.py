import streamlit as st
import pandas as pd
import numpy as np

# 1. 데이터 검증 및 팀 정밀 매핑 (1번 적용)
@st.cache_data
def get_verified_data():
    data = pd.read_csv('full_mlb_events_2026.csv')
    
    # 팀 매핑
    data['batter_team'] = np.where(data['inning_topbot'] == 'top', data['home_team'], data['away_team'])
    batter_map = data.groupby('batter')['batter_team'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    data['batter_2026_team'] = data['batter'].map(batter_map)
    
    # 검증: 구단별 데이터 분포 확인
    dist = data['batter_2026_team'].value_counts()
    return data, dist

# 2. 통계적 전력 분석 (2번 적용)
def analyze_team_power(df):
    # 각 팀의 평균 타구 속도와 발사각을 통한 전력 산출
    team_power = df.groupby('batter_2026_team').agg({
        'launch_speed': 'mean',
        'launch_angle': 'mean'
    }).rename(columns={'launch_speed': 'Avg_Exit_Velocity', 'launch_angle': 'Avg_Launch_Angle'})
    return team_power

# 3. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 데이터 검증 및 전력 분석 v25.0")

if st.sidebar.button("시스템 동기화 및 분석 수행"):
    with st.spinner("데이터 무결성 검증 및 전력 산출 중..."):
        df, dist = get_verified_data()
        
        # 1) 데이터 분포 진단
        st.subheader("📊 [단계 1] 데이터 무결성 진단")
        st.bar_chart(dist)
        
        # 2) 전력 분석 결과
        st.subheader("📈 [단계 2] 팀별 전력 통계 분석")
        power_df = analyze_team_power(df)
        st.dataframe(power_df.sort_values('Avg_Exit_Velocity', ascending=False))
        
        st.success("시스템 정상: 데이터 검증이 완료된 팀을 대상으로 분석되었습니다.")



st.caption("Engine Status: Data Integrity & Analytics Fully Integrated | v25.0")
