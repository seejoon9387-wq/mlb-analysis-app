import streamlit as st
import pandas as pd
import requests

st.title("⚾ MLB 최종 데이터 추출기")

if st.button("데이터 최종 추출"):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": "592450"}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get('body', {})
    
    # opponents 데이터가 리스트인지 확인
    opponents = data.get('opponents', [])
    
    if isinstance(opponents, list):
        # 리스트 안에 든 모든 데이터를 하나로 합침
        all_data = []
        for item in opponents:
            # 각 항목이 또 리스트라면 안으로 들어감
            if isinstance(item, list):
                all_data.extend(item)
            else:
                all_data.append(item)
        
        if all_data:
            df = pd.DataFrame(all_data)
            st.write(f"### 총 {len(df)}개의 데이터를 성공적으로 불러왔습니다.")
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("리스트는 존재하나 내용이 비어있습니다.")
    else:
        st.error("데이터 구조가 리스트가 아닙니다.")
