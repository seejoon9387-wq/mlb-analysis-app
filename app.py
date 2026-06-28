# 버전: v76.0
# 목적: 다운로드 없이 화면에서 즉시 데이터를 수집하고 분석
import streamlit as st
from pybaseball import statcast

st.title("⚾ 데이터 즉시 분석기 (v76.0)")

if st.button("2024년 4월 데이터 수집 및 즉시 확인"):
    with st.spinner("수집 중..."):
        try:
            # 데이터를 변수(df)에 바로 담기 (파일 저장 과정 생략)
            df = statcast(start_dt="2024-04-01", end_dt="2024-04-10")
            
            # 화면에 바로 데이터프레임 출력
            st.success("수집 성공!")
            st.dataframe(df) # 여기서 직접 데이터를 볼 수 있습니다.
            
            # 이 데이터를 가지고 바로 분석 시작
            st.write(f"총 {len(df)}개의 투구 데이터 확인됨")
            
        except Exception as e:
            st.error(f"오류: {e}")
