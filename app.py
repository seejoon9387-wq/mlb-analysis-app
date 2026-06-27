import streamlit as st
import pandas as pd
import requests

# 페이지 구성
st.set_page_config(layout="wide")
st.title("⚾ MLB 상세 분석 시스템")

# [고정 레이아웃]
col_left, col_right = st.columns([1, 3])

with col_left:
    st.subheader("분석 도구")
    player_id = st.text_input("선수 ID", value="592450")
    btn_search = st.button("데이터 조회")

with col_right:
    st.subheader("데이터 대시보드")
    
    if btn_search:
        # API 호출 부분
        API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
        HOST = "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
        url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}
        params = {"playerID": player_id}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json().get('body', {})
            opponents = data.get('opponents', {})
            
            # [핵심] 쪼개진 opponents 데이터를 하나로 합치기
            all_opponents = []
            for key in opponents:
                # 각 리스트 내의 항목들을 하나씩 추가
                if isinstance(opponents[key], list):
                    all_opponents.extend(opponents[key])
            
            if all_opponents:
                df = pd.DataFrame(all_opponents)
                st.dataframe(df, use_container_width=True)
                st.success(f"선수 {player_id}에 대한 상대 전적 데이터를 성공적으로 불러왔습니다.")
            else:
                st.warning("상대 전적 데이터(opponents)가 비어있습니다.")
        else:
            st.error("데이터 호출 실패")
