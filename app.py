import streamlit as st
import pandas as pd
import requests
from datetime import date

# 페이지 설정
st.set_page_config(page_title="MLB 상세 분석 대시보드", layout="wide")

st.title("⚾ MLB 상세 통계 분석 대시보드")

# 사이드바: 분석 환경 설정
with st.sidebar:
    st.header("⚙️ 분석 설정")
    player_id = st.text_input("선수 ID", value="592450")
    
    # 날짜 범위 설정
    start_date = st.date_input("시작 날짜", value=date(2026, 1, 1))
    end_date = st.date_input("종료 날짜", value=date.today())
    
    # 범위 슬라이더 (예: 타수 범위 조절 등)
    min_at_bats = st.slider("최소 타수(AB) 설정", 0, 500, 10)
    
    st.divider()
    analyze_btn = st.button("🚀 수동 분석 실행")

# 메인 영역
if analyze_btn:
    with st.spinner("데이터를 가져오는 중..."):
        # API 호출 및 데이터 처리 로직
        API_KEY = "03e8cebecemsh5ae22ee471e893ap10ec28jsn96d260298651"
        url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
        params = {"playerID": player_id}
        headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json().get('body', {})
            opponents = data.get('opponents', [])
            
            all_data = []
            for item in opponents:
                if isinstance(item, list): all_data.extend(item)
                else: all_data.append(item)
            
            if all_data:
                df = pd.json_normalize(all_data)
                
                # 데이터 필터링: 최소 타수 적용
                if 'AB' in df.columns:
                    df['AB'] = pd.to_numeric(df['AB'], errors='coerce')
                    df = df[df['AB'] >= min_at_bats]
                
                st.subheader(f"📊 분석 결과 (데이터 {len(df)}건)")
                
                # 핵심 컬럼만 표시
                cols = [c for c in ['batterName', 'pitcherName', 'H', 'AB', 'AVG', 'OPS', 'HR'] if c in df.columns]
                st.dataframe(df[cols].sort_values(by='OPS', ascending=False), use_container_width=True)
            else:
                st.warning("조회된 데이터가 없습니다.")
        except Exception as e:
            st.error(f"분석 중 오류 발생: {e}")
else:
    st.info("왼쪽 패널에서 선수 ID와 분석 조건을 설정한 후 **'수동 분석 실행'** 버튼을 누르세요.")
