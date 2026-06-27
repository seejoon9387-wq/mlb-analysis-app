import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("⚾ MLB 데이터 강제 분해기")

if st.button("데이터 구조 완벽 분해"):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": "592450"}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get('body', {})
    opponents = data.get('opponents', [])
    
    all_data = []
    for item in opponents:
        if isinstance(item, list): all_data.extend(item)
        else: all_data.append(item)
    
    # [핵심 변경사항]
    # 단순히 DataFrame으로 만드는 대신, 중첩된 JSON을 쪼개는 작업 수행
    df = pd.json_normalize(all_data)
    
    st.write("### 분해 완료된 데이터")
    st.dataframe(df, use_container_width=True)
    
    # 데이터가 어떻게 쪼개졌는지 확인용
    st.write("추출된 컬럼들:", df.columns.tolist())
