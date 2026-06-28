import streamlit as st
import pandas as pd
from pybaseball import schedule_and_record
from sklearn.ensemble import RandomForestClassifier

# 1. 데이터 병합 최적화 엔진 (1번 적용)
@st.cache_data
def get_ready_to_train_data():
    statcast = pd.read_csv('full_mlb_events_2026.csv')
    statcast['game_date'] = pd.to_datetime(statcast['game_date'])
    # 전체 팀 데이터를 병합하여 데이터셋 규모 확대
    schedule = schedule_and_record(2026, 'LAD') # 필요시 팀 리스트 루프 처리
    schedule['Date'] = pd.to_datetime(schedule['Date'])
    schedule['target'] = schedule['W/L'].apply(lambda x: 1 if x == 'W' else 0)
    return pd.merge(statcast, schedule, left_on='game_date', right_on='Date', how='inner')

# 2. 승리 기여도 분석 및 예측 모델 (2번 적용)
def run_model_and_report(df):
    features = ['release_speed', 'launch_speed', 'launch_angle', 'estimated_ba_using_speedangle']
    X = df[features].fillna(0)
    y = df['target']
    model = RandomForestClassifier(n_estimators=100).fit(X, y)
    return model, features

# 

# 3. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 승리 기여도 진단 엔진 v19.2")

if st.sidebar.button("데이터 분석 및 진단 시작"):
    with st.spinner("데이터 병합 및 AI 학습 중..."):
        df = get_ready_to_train_data()
        model, feats = run_model_and_report(df)
        
        # 기여도 리포트 출력
        st.subheader("📊 핵심 승리 기여 지표 (Feature Importance)")
        importance = pd.DataFrame({'Metric': feats, 'Impact': model.feature_importances_})
        st.bar_chart(importance.set_index('Metric'))
        
        st.success("데이터 진단 완료: 위 지표들이 현재 팀 승률에 가장 큰 영향을 주고 있습니다.")
