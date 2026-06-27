import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("⚾ MLB 선수 상세 통계 대시보드")

if st.button("데이터 강제 펼치기"):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": "592450"}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get('body', {})
    
    # opponents 항목들은 리스트 형태의 딕셔너리들로 구성됨
    opponents = data.get('opponents', {})
    
    all_rows = []
    # 딕셔너리의 각 키값(예: 0-99, 100-199...)에 있는 리스트를 모두 합침
    for key in opponents:
        if isinstance(opponents[key], list):
            all_rows.extend(opponents[key])
    
    if all_rows:
        df = pd.DataFrame(all_rows)
        st.success(f"총 {len(df)}개의 데이터 항목을 불러왔습니다.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("데이터가 여전히 비어있습니다. API 응답 제한 때문일 수 있습니다.")
