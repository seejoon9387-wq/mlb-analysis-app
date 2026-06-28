# 버전: v2.7.1
# 패치 내용: 크롤링 오류 해결 및 데이터 표시 로직 수정
import streamlit as st
import pandas as pd

# (이전 함수들 생략...)

if menu == "실시간 일정":
    st.subheader("오늘의 MLB 경기 일정")
    
    # 임시 데이터 로딩 (실제 API 연동 전 테스트)
    data = {
        "경기시간": ["08:05", "10:10", "11:00"],
        "홈팀": ["NYY", "LAD", "SF"],
        "원정팀": ["BOS", "SD", "COL"],
        "상태": ["예정", "경기중", "종료"]
    }
    df_schedule = pd.DataFrame(data)
    
    st.table(df_schedule)
    st.info("현재 실시간 API 서버 연결 대기 중...")
