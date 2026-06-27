import streamlit as st
import requests
import pandas as pd

# 1. 구독 확인: https://rapidapi.com/odds-feed-odds-feed-default/api/odds-feed/pricing
# 2. 아래 엔드포인트와 헤더를 대시보드의 'Code Snippet'과 똑같이 맞췄습니다.

API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"

def get_data_from_api():
    url = "https://odds-feed.p.rapidapi.com/api/v1/markets/feed"
    # 403 에러 방지를 위해 필수 헤더를 명확히 고정합니다.
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "odds-feed.p.rapidapi.com"
    }
    # 파라미터는 API 문서에서 요구하는 최소한만 넣습니다.
    params = {"placing": "LIVE", "market_name": "1X2", "bet_type": "BACK", "page": "0"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        # 403 에러 발생 시 상세 메시지 출력
        if response.status_code == 403:
            st.error("403 Forbidden: API 구독 상태를 확인하거나, 호출 제한을 확인하세요.")
            st.write("RapidAPI 대시보드에서 'Subscribe to Test'를 완료했는지 꼭 확인해주세요.")
            return None
        return response.json()
    except Exception as e:
        st.error(f"연결 오류: {e}")
        return None

# UI는 그대로 유지
st.title("⚾ MLB AI 분석 시스템")
# ... (상단 설정 및 좌측 분석창 코드) ...

with st.sidebar:
    st.write("API 상태 확인")
    if st.button("배당 데이터 갱신"):
        result = get_data_from_api()
        if result:
            st.write(result)
