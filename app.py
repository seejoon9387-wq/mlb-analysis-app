import streamlit as st
import pandas as pd
import io

# 1. 파일 로드 (업로드하신 파일을 직접 읽습니다)
@st.cache_data
def load_data():
    df = pd.read_csv("mlb_final_master.csv")
    df.columns = [c.strip().lower() for c in df.columns]
    # 날짜를 문자열로 고정하여 비교 오류 차단
    df['date'] = df['date'].astype(str)
    return df

df = load_data()

st.title("⚾ 데이터 검증 및 매칭 리포트")

# [검증 1단계] 데이터 샘플 확인 (진실의 방)
with st.expander("1단계: 데이터 원본 확인 (최근 10행)"):
    st.write("실제 CSV 파일에 저장된 데이터입니다. 점수가 0인지 숫자인지 직접 확인하세요.")
    st.dataframe(df.tail(10))

# [검증 2단계] 날짜별 데이터 구조 확인
st.write("---")
st.write("### 2단계: 선택한 날짜의 상세 구조")
selected_date = st.text_input("확인할 날짜 입력 (예: 2026-06-28):", value="2026-06-28")

match_data = df[df['date'] == selected_date]

if not match_data.empty:
    st.success(f"{selected_date}에 해당하는 데이터가 {len(match_data)}건 발견되었습니다.")
    # 실제 컬럼명과 점수 매칭 여부 확인
    st.table(match_data[['home_team', 'home_score', 'away_team', 'away_score']])
else:
    st.warning(f"{selected_date} 데이터가 없습니다. (데이터 내 존재하는 날짜 예시: {df['date'].unique()[-5:]})")

# [검증 3단계] 데이터 소스 및 점수 정합성 평가
st.write("---")
st.write("### 3단계: 점수 정합성 평가")
if not match_data.empty:
    # 0점인 데이터가 있는지 확인
    zero_scores = match_data[(match_data['home_score'] == 0) & (match_data['away_score'] == 0)]
    if len(zero_scores) > 0:
        st.error(f"주의: {len(zero_scores)}개의 경기가 0:0으로 기록되어 있습니다. (데이터 누락 또는 경기 전)")
    else:
        st.info("모든 경기에 점수가 정상적으로 기록되어 있습니다.")
