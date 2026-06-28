import streamlit as st
import pandas as pd
import requests
import io

FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"

@st.cache_data
def load_and_clean_data(fid):
    url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
    res = requests.get(url)
    df = pd.read_csv(io.BytesIO(res.content))
    df.columns = [c.strip().lower() for c in df.columns]
    
    # 1. 날짜를 무조건 YYYY-MM-DD 문자열로 변환 (시간 정보 원천 봉쇄)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    
    # 2. 점수 타입 고정
    df['home_score'] = pd.to_numeric(df['home_score'], errors='coerce').fillna(0).astype(int)
    df['away_score'] = pd.to_numeric(df['away_score'], errors='coerce').fillna(0).astype(int)
    
    return df

st.set_page_config(layout="wide")
st.title("⚾ MLB 최종 경기 결과 대시보드")

df = load_and_clean_data(FILE_ID_GAME)

# 🗓️ 달력 선택
selected_date = st.date_input("조회할 날짜를 선택하세요:")
# 선택한 날짜를 데이터와 같은 YYYY-MM-DD 문자열로 변환
str_selected_date = selected_date.strftime('%Y-%m-%d')

# 3. 데이터 필터링 (문자열끼리 정확히 비교)
match_data = df[df['date'] == str_selected_date]

if not match_data.empty:
    st.success(f"{str_selected_date} 경기 결과 ({len(match_data)}건)")
    st.dataframe(match_data, use_container_width=True)
else:
    st.warning(f"{str_selected_date}에 등록된 데이터가 없습니다.")
    st.write("---")
    st.write("### 현재 데이터에 존재하는 날짜 목록 (최근 5일)")
    st.write(df['date'].unique()[-5:]) # 데이터에 실제 있는 날짜 확인용
