import streamlit as st
import pandas as pd
import requests

# 1. 페이지 레이아웃 고정
st.set_page_config(page_title="MLB AI", layout="wide")

# 2. 고정 헤더
st.title("⚾ MLB 분석 대시보드")
st.markdown("---")

# 3. 레이아웃 강제 분할 (사라지지 않음)
col_a, col_b = st.columns([1, 2])

# 왼쪽 분석 엔진 영역
with col_a:
    st.subheader("분석 설정")
    player_id = st.text_input("선수 ID 입력", "592450")
    run_btn = st.button("분석 실행")

# 오른쪽 배당 및 데이터 영역
with col_b:
    st.subheader("결과 출력")
    
    if run_btn:
        # 데이터 호출 로직
        API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
        HOST = "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
        url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
        
        try:
            response = requests.get(url, headers={"x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST}, params={"playerID": player_id})
            
            if response.status_code == 200:
                data = response.json()
                # 데이터 구조 확인 및 파싱
                opponents = data.get('body', {}).get('opponents', {})
                if opponents:
                    # 모든 데이터를 하나로 병합
                    all_data = []
                    for k in opponents:
                        if isinstance(opponents[k], list): all_data.extend(opponents[k])
                    
                    df = pd.DataFrame(all_data)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("데이터는 성공적으로 가져왔으나, 안에 담긴 'opponents' 내용이 비어있습니다.")
            else:
                st.error(f"API 응답 실패: {response.status_code}")
        except Exception as e:
            st.error(f"오류 발생: {e}")
    else:
        st.info("선수 ID를 입력하고 '분석 실행' 버튼을 누르세요.")
