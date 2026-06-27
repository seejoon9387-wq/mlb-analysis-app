import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("⚾ MLB 데이터 강제 호출")

if st.button("데이터 조회"):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": "592450"}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get('body', {})
    
    # 1. opponents가 존재하는지, 딕셔너리인지 확인
    opponents = data.get('opponents')
    
    if opponents is None:
        st.warning("데이터가 없습니다 (opponents is None)")
    elif isinstance(opponents, dict):
        all_rows = []
        for key, value in opponents.items():
            if isinstance(value, list):
                all_rows.extend(value)
        
        if all_rows:
            df = pd.DataFrame(all_rows)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("데이터는 있으나 리스트 안이 비어있습니다.")
    elif isinstance(opponents, list):
        # opponents가 바로 리스트인 경우 대응
        df = pd.DataFrame(opponents)
        st.dataframe(df, use_container_width=True)
    else:
        st.write("데이터 구조를 파악할 수 없습니다:", type(opponents))
        st.write(opponents)
