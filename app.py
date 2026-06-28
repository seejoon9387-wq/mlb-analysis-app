import streamlit as st
import pandas as pd
import numpy as np

# 1. 데이터 검증 및 필터링 엔진 (데이터 무결성 최우선 적용)
@st.cache_data
def get_verified_data(min_samples=100):
    data = pd.read_csv('full_mlb_events_2026.csv')
    
    # 팀 매핑
    data['batter_team'] = np.where(data['inning_topbot'] == 'top', data['home_team'], data['away_team'])
    batter_map = data.groupby('batter')['batter_team'].agg(lambda x: x.mode()[0] if not x.mode().empty else 'Unknown')
    data['batter_2026_team'] = data['batter'].map(batter_map)
    
    # 데이터 분포 확인
    dist = data['batter_2026_team'].value_counts()
    
    # 데이터가 부족한 팀 필터링 (신뢰도 보장)
    reliable_teams = dist[dist >= min_samples].index
    filtered_data = data[data['batter_2026_team'].isin(reliable_teams)]
    
    return filtered_data, dist, reliable_teams

# 2. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 데이터 무결성 검증 시스템 v26.0")

if st.sidebar.button("데이터 검증 및 신뢰도 분석"):
    with st.spinner("구단별 데이터 표본 검사 중..."):
        df, dist, reliable = get_verified_data()
        
        st.subheader("📊 데이터 무결성 진단 리포트")
        col1, col2 = st.columns(2)
        
        # 검증 통계 시각화
        col1.write("구단별 데이터 수집 분포")
        col1.bar_chart(dist)
        
        # 신뢰도 평가
        col2.write("분석 적합 구단 리스트 (표본 100건 이상)")
        col2.dataframe(reliable)
        
        if len(reliable) < 30:
            st.warning(f"⚠️ 경고: {30 - len(reliable)}개 구단의 데이터가 부족하여 분석의 편향이 발생할 수 있습니다.")
        else:
            st.success("✅ 모든 구단 데이터가 충분하여 정밀 분석이 가능합니다.")
