import streamlit as st
import pandas as pd

# 1. 데이터 연산 로직 (화면 출력 명령어 없음)
def get_pitcher_summary(df_pitcher, pitcher_name):
    """
    제공된 투수 데이터프레임에서 특정 투수의 주요 지표를 계산하여 반환
    """
    # 데이터 필터링 (순수 연산)
    pitcher_data = df_pitcher[df_pitcher['last_name, first_name'].str.contains(pitcher_name, case=False, na=False)]
    
    if pitcher_data.empty:
        return None
    
    # 핵심 지표 추출 (예시)
    summary = {
        'FIP': pitcher_data[pitcher_data['Metric'] == 'fip']['fip'].mean(),
        'Whiff%': pitcher_data[pitcher_data['Metric'] == 'whiff_pct']['whiff_pct'].mean()
    }
    return summary

# 2. 메인 화면 로직 (결과 표시 위주)
st.title("⚾ MLB 투수 분석기")

# 사용자 입력
pitcher_input = st.text_input("분석할 투수 이름 입력")

if st.button("분석 실행"):
    with st.spinner("데이터를 분석 중입니다..."):
        # 여기서 앞서 만든 df_pitcher를 활용 (실제 환경에선 미리 저장된 CSV를 로드 권장)
        # 예시로 df_pitcher가 메모리에 있다고 가정
        result = get_pitcher_summary(df_pitcher, pitcher_input)
    
    if result:
        # 3. 결과값만 깔끔하게 표시
        st.subheader(f"📊 {pitcher_input} 분석 결과")
        col1, col2 = st.columns(2)
        col1.metric("평균 FIP", f"{result['FIP']:.2f}")
        col2.metric("평균 Whiff %", f"{result['Whiff%']:.1f}%")
    else:
        st.error("데이터를 찾을 수 없습니다.")
