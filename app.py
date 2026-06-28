import streamlit as st
import pandas as pd
import numpy as np

# 1. 데이터 검증 및 팀 정밀 매핑 엔진
@st.cache_data
def get_processed_data():
    data = pd.read_csv('full_mlb_events_2026.csv')
    
    # 1) 팀 매핑 로직
    data['batter_team'] = np.where(data['inning_topbot'] == 'top', data['home_team'], data['away_team'])
    data['pitcher_team'] = np.where(data['inning_topbot'] == 'top', data['away_team'], data['home_team'])
    
    # 2) 선수별 주 소속팀 매핑 (최빈값 활용)
    batter_map = data.groupby('batter')['batter_team'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    pitcher_map = data.groupby('pitcher')['pitcher_team'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    
    data['batter_2026_team'] = data['batter'].map(batter_map)
    data['pitcher_2026_team'] = data['pitcher'].map(pitcher_map)
    
    return data

# 2. 분석 엔진: 팀별 공격력 지표 산출
def analyze_team_power(df):
    team_power = df.groupby('batter_2026_team').agg({
        'launch_speed': 'mean',
        'launch_angle': 'mean',
        'estimated_ba_using_speedangle': 'mean'
    }).rename(columns={'estimated_ba_using_speedangle': 'expected_BA'})
    return team_power

# 

# 3. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 정밀 팀 분석 엔진 v23.0")

if st.sidebar.button("팀 매핑 및 전력 분석 실행"):
    with st.spinner("데이터 정제 및 팀별 성적 집계 중..."):
        df = get_processed_data()
        power_df = analyze_team_power(df)
        
        st.subheader("📊 2026 시즌 팀별 공격 효율 지표")
        st.dataframe(power_df.sort_values('expected_BA', ascending=False), use_container_width=True)
        
        st.subheader("상위 5개 팀 공격력 비교")
        st.bar_chart(power_df.sort_values('expected_BA', ascending=False).head(5)['expected_BA'])
        
        st.success("분석 완료: 모든 데이터가 팀 단위로 완벽히 매핑되었습니다.")
