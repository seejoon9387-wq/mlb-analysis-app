import streamlit as st
import pandas as pd

# 1. 구글 드라이브 데이터 로드
def get_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    return pd.read_csv(url)

st.title("MLB 경기 결과 조회")

# 데이터 불러오기
df = get_data()

# 2. 팀 검색창
search_team = st.text_input("팀 이름을 입력하세요 (예: Dodgers, Yankees):")

if st.button("조회"):
    if search_team:
        # 검색어가 포함된 데이터 필터링
        res = df[
            df['home_team'].str.contains(search_team, case=False, na=False) | 
            df['away_team'].str.contains(search_team, case=False, na=False)
        ]
        
        if not res.empty:
            st.table(res)
        else:
            st.write("결과가 없습니다. 팀 이름을 다시 확인해주세요.")
    else:
        st.write("팀 이름을 입력하세요.")
