import streamlit as st
import requests

st.title("⚾ 데이터 디버깅 최종 단계")

if st.button("데이터 구조 100% 덤프"):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": "592450"}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    # 여기서 데이터를 아주 자세하게 풀어냅니다.
    st.write("### 상세 데이터 확인")
    st.write(data) 
    
    # 특히 body 안의 opponents를 하나씩 찍어봅니다.
    if 'body' in data and 'opponents' in data['body']:
        st.write("---")
        st.write("Opponents 항목 키 확인:")
        st.write(data['body']['opponents'].keys())
