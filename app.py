import streamlit as st
import pandas as pd

@st.cache_data
def get_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    # 데이터의 첫 번째 열을 날짜로 인식
    df.columns = ['date', 'home_team', 'away_team', 'home_score', 'away_score']
    df['date'] = pd.to_datetime(df['date'])
    return df

st.title("⚾ 날짜별 경기 결과 조회")

df = get_data()
selected_date = st.date_input("날짜 선택:")

if st.button("조회"):
    target = pd.Timestamp(selected_date)
    result = df[df['date'] == target]
    
    if not result.empty:
        st.table(result)
    else:
        st.write("해당 날짜에 기록된 데이터가 없습니다.")
