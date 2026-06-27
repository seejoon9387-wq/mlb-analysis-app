import streamlit as st
import pandas as pd
import requests

# 페이지 설정
st.set_page_config(page_title="MLB 통계 분석 대시보드", layout="wide")

st.title("⚾ MLB 선수 상세 통계 분석")

# 사이드바 설정 (컨트롤 영역)
with st.sidebar:
    st.header("데이터 제어")
    player_id = st.text_input("선수 ID 입력", value="592450")
    run_btn = st.button("통계 데이터 불러오기")

# 메인 화면: 통계 대시보드
st.subheader("상대 투타 전적 통계")

if run_btn:
    API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
    url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
    params = {"playerID": player_id}
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
    
    try:
        with st.spinner("데이터를 분석 중입니다..."):
            response = requests.get(url, headers=headers, params=params)
            data = response.json().get('body', {})
            opponents = data.get('opponents', [])
            
            # 데이터 평탄화
            all_data = []
            for item in opponents:
                if isinstance(item, list): all_data.extend(item)
                else: all_data.append(item)
            
            if all_data:
                df = pd.json_normalize(all_data)
                
                # 가독성을 위해 핵심 컬럼만 추출 (데이터에 존재하는지 확인 후)
                target_cols = ['batterName', 'pitcherName', 'H', 'AB', 'AVG', 'OPS', 'HR', 'RBI']
                available_cols = [c for c in target_cols if c in df.columns]
                
                if available_cols:
                    # 표 출력
                    st.dataframe(df[available_cols].sort_values(by='OPS', ascending=False), use_container_width=True)
                else:
                    st.write("상세 통계:", df)
                
                st.success(f"총 {len(df)}개의 기록을 분석했습니다.")
            else:
                st.warning("데이터가 없습니다. 선수 ID를 확인해주세요.")
                
    except Exception as e:
        st.error(f"오류 발생: {e}")
else:
    st.info("왼쪽 사이드바에서 선수 ID를 입력하고 '통계 데이터 불러오기'를 누르세요.")
