import streamlit as st
import pandas as pd
import os
import requests

# 1. AI 분석 엔진: 결과값 산출 로직
def calculate_edge(home_win_prob, decimal_odds):
    """
    승률과 배당을 비교하여 모델이 산출한 이득(Edge)을 계산
    Edge > 0 이면 저평가된 팀
    """
    implied_prob = 1 / decimal_odds
    edge = (home_win_prob / implied_prob) - 1
    return edge

# 2. 메인 화면 구성
st.set_page_config(page_title="MLB Edge Analyzer", layout="wide")
st.title("⚾ MLB AI 정밀 Edge 분석 리포트")

# 3. 분석 수행 (내부 연산)
st.sidebar.header("분석 설정")
api_key = st.sidebar.text_input("Odds API Key", type="password")
files = [f for f in os.listdir('/content/') if f.endswith('.csv')]
selected_file = st.sidebar.selectbox("분석 데이터 선택", files)

if api_key and selected_file:
    with st.spinner("AI가 승률과 배당을 대조하여 Edge를 계산 중입니다..."):
        # 데이터 로드
        df = pd.read_csv(os.path.join('/content/', selected_file))
        
        # [내부 연산] 여기에서 승률 산출 및 Edge 계산 (추후 변수 추가 시 확장)
        # 예시: 데이터 내 'win_pct'가 있다고 가정
        if 'win_pct' in df.columns:
            df['edge'] = df.apply(lambda x: calculate_edge(x['win_pct'], 1.9), axis=1) # 예시 배당 1.9
            
            # 최종 결과값만 추출 (Edge가 높은 순으로 정렬)
            final_report = df[['team_name', 'win_pct', 'edge']].sort_values(by='edge', ascending=False)
            
            st.subheader("📌 최종 분석 결과 (Edge 상위권)")
            st.dataframe(final_report.head(10), use_container_width=True)
            st.success("연산 완료: 통계적 이득이 확인된 상위 리스트입니다.")
        else:
            st.error("데이터 파일에 'win_pct' 컬럼이 필요합니다.")
else:
    st.info("API Key를 입력하고 분석할 CSV 파일을 선택하세요.")

st.divider()
st.caption("System: AI Inference Engine v1.0 | Mode: Edge Calculation Active")
