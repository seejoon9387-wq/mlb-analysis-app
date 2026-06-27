import streamlit as st
import pandas as pd
import requests

st.title("⚾ MLB 투타 상세 전적 (OPS 분석)")

if st.button("통계 데이터 정리하기"):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": "592450"}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json().get('body', {})
    
    # 821개의 데이터를 가져와서 표로 변환
    all_data = []
    for key, value in data.get('opponents', {}).items():
        if isinstance(value, list): all_data.extend(value)
    
    df = pd.json_normalize(all_data)
    
    # 핵심 통계 항목만 골라내기 (데이터프레임에 실제 존재하는 컬럼명으로 수정 필요)
    # 0, 1 같은 숫자가 아닌 실제 통계값이 적힌 컬럼명을 찾아야 합니다.
    target_cols = ['batterName', 'pitcherName', 'H', 'AB', 'AVG', 'OPS', 'HR']
    
    # 존재하는 컬럼만 골라서 표 생성
    available_cols = [c for c in target_cols if c in df.columns]
    
    if available_cols:
        st.dataframe(df[available_cols].sort_values(by='OPS', ascending=False), use_container_width=True)
    else:
        st.write("사용 가능한 컬럼 목록:", df.columns.tolist())
