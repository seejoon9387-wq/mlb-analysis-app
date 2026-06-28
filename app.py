import streamlit as st
import pandas as pd

# 1. 데이터 로드 (컬럼 개수 상관없이 있는 그대로 읽기)
@st.cache_data
def get_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    return pd.read_csv(url)

st.title("⚾ MLB 경기 결과 조회")

df = get_data()

# 2. 데이터에 어떤 컬럼이 있는지 확인 (사용자님 데이터 구조 확인용)
st.write("현재 데이터의 컬럼 정보:", list(df.columns))

# 3. 날짜 컬럼을 수동으로 선택하도록 함
selected_date_col = st.selectbox("날짜가 들어있는 컬럼을 선택하세요:", df.columns)
selected_date = st.date_input("조회할 날짜 선택:")

if st.button("조회"):
    # 선택한 컬럼을 날짜 형식으로 변환
    df['temp_date'] = pd.to_datetime(df[selected_date_col], errors='coerce')
    
    # 달력에서 고른 날짜와 매칭되는 행만 가져오기
    target = pd.Timestamp(selected_date)
    result = df[df['temp_date'].dt.date == target.date()]
    
    if not result.empty:
        st.table(result)
    else:
        st.write("선택하신 날짜에 일치하는 기록이 없습니다.")
