import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout="wide")
st.title("⚾ MLB 선수 상세 통계 대시보드")

if st.button("데이터 강제 표 변환"):
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": "592450"}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        # 'body' 안에 있는 'opponents' 데이터를 타겟팅
        body = data.get('body', {})
        opponents = body.get('opponents', {})

        # 데이터를 리스트로 변환 (모든 키의 값을 하나로 합침)
        all_records = []
        if isinstance(opponents, dict):
            for key in opponents:
                if isinstance(opponents[key], list):
                    all_records.extend(opponents[key])
        
        # 표로 변환
        if all_records:
            df = pd.DataFrame(all_records)
            # 강제로 표 형태로 렌더링
            st.table(df.head(20)) # 너무 길면 안 보이니 일단 상위 20개만
        else:
            st.write("데이터 구조가 표로 출력할 수 없는 형태입니다. 원본을 확인하세요:")
            st.json(data)
            
    except Exception as e:
        st.error(f"오류: {e}")
