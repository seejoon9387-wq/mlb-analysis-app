import streamlit as st
import pandas as pd

# 파일 로드 (업로드된 파일 사용)
df = pd.read_csv("mlb_final_master.csv")
df.columns = [c.strip().lower() for c in df.columns]

st.title("⚾ MLB 경기 결과 정밀 조회")

# 오늘 날짜
today = "2026-06-29"
selected_date = st.text_input("날짜 입력 (YYYY-MM-DD):", value=today)

# [핵심] 해당 날짜 데이터만 필터링
match_data = df[df['date'] == selected_date]

if not match_data.empty:
    st.write(f"### {selected_date} 경기 결과")
    # 점수가 0이면 '경기 전/진행 중', 숫자가 있으면 그대로 표시
    # home_score, away_score가 제대로 매칭되는지 눈으로 확인
    st.table(match_data[['home_team', 'home_score', 'away_team', 'away_score', 'venue']])
    
    # 0점 확인 로직 추가
    if (match_data['home_score'] == 0).all() and (match_data['away_score'] == 0).all():
        st.warning("경기가 아직 종료되지 않았거나, 데이터 업데이트 전입니다.")
else:
    st.error("해당 날짜에 데이터가 없습니다.")
