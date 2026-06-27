import streamlit as st
import pandas as pd
import requests

# 페이지 레이아웃 고정
st.set_page_config(page_title="MLB AI Analyst", layout="wide")

# UI 프레임 생성 (데이터 유무와 상관없이 항상 고정)
st.title("⚾ MLB 배당 및 데이터 대시보드")
col_ui, col_data = st.columns([1, 3])

with col_ui:
    st.subheader("데이터 컨트롤")
    run_btn = st.button("데이터 새로고침")

with col_data:
    st.subheader("실시간 배당/데이터 대시보드")
    # 데이터 출력용 빈 영역 고정
    data_placeholder = st.empty()
    data_placeholder.info("데이터를 불러오려면 '데이터 새로고침'을 누르세요.")

# 데이터 호출 로직
if run_btn:
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    params = {"playerID": "592450"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json().get('body', {})
            opponents = data.get('opponents', [])
            
            # [수정된 부분] 리스트 타입 확인 후 처리
            if isinstance(opponents, list):
                if len(opponents) > 0:
                    df = pd.DataFrame(opponents)
                    data_placeholder.dataframe(df, use_container_width=True)
                else:
                    data_placeholder.warning("상대 전적 데이터가 비어있습니다.")
            else:
                data_placeholder.error("데이터 형식이 리스트가 아닙니다.")
        else:
            data_placeholder.error(f"API 호출 실패: {response.status_code}")
    except Exception as e:
        data_placeholder.error(f"연결 오류 발생: {e}")
