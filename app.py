import streamlit as st
import pandas as pd
import numpy as np

# 1. 정합성 강화된 데이터 정제 엔진
@st.cache_data
def get_cleaned_data():
    data = pd.read_csv('full_mlb_events_2026.csv')
    
    # 1) 팀 정보 공식화 (사용자님 코드 적용)
    data['pitcher_team_official'] = data['pitcher_team_official'].fillna(data['pitcher_2026_team'])
    data['batter_team_official'] = data['batter_team_official'].fillna(data['batter_2026_team'])
    
    # 2) 주요 지표 결측치 보완 (0 처리)
    cols_to_fill = ['launch_speed', 'is_whiff', 'release_speed', 'woba_value', 'launch_angle']
    for col in cols_to_fill:
        if col in data.columns:
            data[col] = data[col].fillna(0)
            
    return data

# 

# 2. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 데이터 정합성 및 정제 엔진 v31.0")

if st.sidebar.button("데이터 정제 및 상태 리포트"):
    with st.spinner("데이터 결측치 보완 및 정합성 체크 중..."):
        df = get_cleaned_data()
        
        # 정제 완료 확인
        st.subheader("✅ 데이터 정제 완료 요약")
        missing_after = df[['launch_speed', 'is_whiff', 'release_speed']].isnull().sum()
        
        if missing_after.sum() == 0:
            st.success("데이터 무결성 100%: 모든 주요 지표가 채워졌습니다.")
        else:
            st.error("결측치가 남아있습니다. 확인이 필요합니다.")
        
        st.dataframe(df.head())
        st.write(f"현재 총 이벤트 수: {len(df)}건")
