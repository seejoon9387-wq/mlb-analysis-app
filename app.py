import streamlit as st
import pandas as pd
import requests

# 1. UI 구조 보호 (어떤 데이터가 와도 이 틀은 깨지지 않음)
st.set_page_config(layout="wide")
st.title("⚾ MLB 배당 및 데이터 대시보드")

# 레이아웃 고정
col_ui, col_data = st.columns([1, 3])

with col_ui:
    st.subheader("데이터 컨트롤")
    run_btn = st.button("배당 데이터 새로고침")

with col_data:
    st.subheader("실시간 배당/데이터 대시보드")
    
    # 2. 데이터가 있든 없든 표(DataFrame)는 항상 존재함
    # 초기화: 빈 데이터프레임 생성
    placeholder_df = pd.DataFrame(columns=["분류", "값", "상태"])
    
    # 데이터 영역을 담을 컨테이너
    data_container = st.empty()
    data_container.dataframe(placeholder_df, use_container_width=True)

# 3. 데이터 호출 로직 (버튼을 눌러야만 동작)
if run_btn:
    try:
        # RapidAPI 호출
        API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
        url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
        params = {"playerID": "592450"}
        
        response = requests.get(url, headers=headers, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json().get('body', {})
            # 데이터 파싱
            all_data = []
            for k, v in data.get('opponents', {}).items():
                if isinstance(v, list): all_data.extend(v)
            
            if all_data:
                df = pd.DataFrame(all_data)
                data_container.dataframe(df, use_container_width=True) # 표 업데이트
                st.success("데이터 로드 완료!")
            else:
                st.warning("데이터는 수신되었으나 표시할 항목이 없습니다.")
        else:
            st.error(f"API 오류: {response.status_code}")
            
    except Exception as e:
        st.error(f"연결 오류: {e}")
