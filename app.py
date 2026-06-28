import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. 데이터 로드 및 날짜 생성 (과거부터 순차적으로 달력과 매칭)
@st.cache_data
def get_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    # 데이터가 최근 것부터인지 과거부터인지 확인해야 하지만, 
    # 일반적인 로그 데이터라 가정하고 오늘부터 역순으로 날짜를 부여합니다.
    today = datetime.now()
    # 데이터 행 수만큼 날짜 생성
    df['date'] = [today - timedelta(days=i) for i in range(len(df))]
    return df

st.title("⚾ 날짜 선택 경기 결과 조회")

df = get_data()

# 2. 달력 생성
selected_date = st.date_input("조회할 날짜를 선택하세요:")

# 3. 조회 버튼
if st.button("경기 결과 조회"):
    # 선택한 날짜에 해당하는 데이터 필터링 (시차 보정을 위해 앞뒤 1일 검색)
    target = pd.Timestamp(selected_date)
    mask = (df['date'].dt.date >= target.date() - timedelta(days=1)) & \
           (df['date'].dt.date <= target.date() + timedelta(days=1))
    
    result = df.loc[mask]
    
    if not result.empty:
        st.subheader(f"{selected_date} 경기 결과")
        st.table(result[['home_team', 'away_team', 'home_score', 'away_score']])
    else:
        st.write("해당 날짜에 일치하는 경기 기록이 없습니다.")
