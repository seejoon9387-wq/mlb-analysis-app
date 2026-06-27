import streamlit as st
import pandas as pd
import requests

st.title("⚾ 데이터 디버깅 툴")

if st.button("데이터 구조 확인하기"):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": "592450"}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    # 1. 원본 데이터 전체 출력
    st.write("### 원본 JSON 데이터 전체:")
    st.json(data) 
    
    # 2. 데이터가 어디 있는지 파악
    if 'body' in data:
        st.write("### 'body' 내부 데이터:")
        st.write(data['body'])
    else:
        st.write("body 키가 없습니다.")
