import streamlit as st
import pandas as pd
import requests

st.title("⚾ MLB 데이터 정밀 타격")

if st.button("0-99번 데이터 조회"):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    
    # [핵심] 구간별로 요청해야 할 가능성이 큼
    params = {
        "playerID": "592450",
        "start": "0",  # API에 구간 시작점을 알려줌
        "end": "99"    # API에 구간 끝점을 알려줌
    }
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    st.write("### 응답 데이터:")
    st.json(data)
