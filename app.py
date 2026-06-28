import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. 구글 드라이브 데이터 로드
@st.cache_data
def get_master_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    # 데이터셋이 과거부터 순차적이라고 가정하고 '날짜' 가상 컬럼 생성
    # 데이터가 12,314건이므로 2024-01-01부터 순차적으로 날짜를 부여합니다.
    start_date = datetime(2024, 1, 1)
    df['simulated_date'] = [start_date + timedelta(days=i) for i in range(len(df))]
    return df

# 2. UI
st.title("⚾ 데이터셋 기반 경기 기록 조회")
df = get_master_data()

# 3. 달력 선택
selected_date = st.date_input("조회할 날짜를 선택하세요:", datetime(2024, 1, 1))

if st.button("내 데이터에서 결과 조회"):
    # 선택한 날짜에 해당하는 행 필터링
    target_date = pd.Timestamp(selected_date)
    result = df[df['simulated_date'].dt.date == target_date.date()]
    
    if not result.empty:
        st.success(f"{selected_date} 경기 결과")
        st.table(result[['home_team', 'away_team', 'home_score', 'away_score']])
    else:
        st.warning("선택하신 날짜에 해당하는 데이터가 데이터셋에 존재하지 않습니다.")
