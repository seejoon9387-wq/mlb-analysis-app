import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("⚾ MLB 상세 통계 분석 대시보드")

if st.button("데이터 깔끔하게 정리하기"):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": "592450"}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get('body', {})
    opponents = data.get('opponents', [])
    
    # 1. 821개의 데이터를 리스트로 합침
    all_data = []
    for item in opponents:
        if isinstance(item, list): all_data.extend(item)
        else: all_data.append(item)
    
    # 2. DataFrame 생성 후 보기 좋은 항목만 선택
    df = pd.DataFrame(all_data)
    
    # [핵심] 컬럼이 너무 많으면 표가 깨지므로, 자주 쓰는 핵심 항목만 필터링합니다.
    # API 데이터에서 제공하는 필드명(예: 'player', 'H', 'AVG' 등)을 확인하여 아래 리스트에 넣으세요.
    cols_to_show = [col for col in ['playerName', 'H', 'AB', 'AVG', 'HR', 'RBI'] if col in df.columns]
    
    if cols_to_show:
        st.dataframe(df[cols_to_show], use_container_width=True)
    else:
        # 원하는 항목이 없으면 일단 전체를 보기 좋게 출력
        st.dataframe(df, use_container_width=True)

    st.success("이제 표의 헤더(열 이름)를 클릭하면 정렬도 가능합니다!")
