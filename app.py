import streamlit as st
import pandas as pd
import requests
import io
from datetime import datetime, timedelta

FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"

@st.cache_data
def load_and_clean_data(fid):
    url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
    res = requests.get(url)
    df = pd.read_csv(io.BytesIO(res.content))
    df.columns = [c.strip().lower() for c in df.columns]
    
    # 1. 날짜 강제 변환 (시간 정보 제거)
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.date
    
    # 2. 점수 데이터 강제 숫자화 (매우 중요!)
    # 숫자가 아닌 값은 0으로 바꾸고, 정수(int)로 변환
    df['home_score'] = pd.to_numeric(df['home_score'], errors='coerce').fillna(0).astype(int)
    df['away_score'] = pd.to_numeric(df['away_score'], errors='coerce').fillna(0).astype(int)
    
    # 3. 데이터 정렬 (날짜 순)
    df = df.sort_values(by='date')
    return df

st.set_page_config(layout="wide")
st.title("⚾ MLB 최종 경기 결과 대시보드")

df = load_and_clean_data(FILE_ID_GAME)

# 오늘 날짜 (KST 기준)
today_kst = datetime.utcnow().date() + timedelta(hours=9)
selected_date = st.date_input("조회할 날짜를 선택하세요:", value=today_kst)

# 데이터 필터링
match_data = df[df['date'] == selected_date]

if not match_data.empty:
    st.success(f"{selected_date} 경기 결과 ({len(match_data)}건)")
    
    # 점수 매칭이 잘 보이는 표 구성
    display_df = match_data[['date', 'home_team', 'home_score', 'away_team', 'away_score', 'venue']]
    st.dataframe(display_df, use_container_width=True)
else:
    st.warning(f"{selected_date}에는 등록된 경기 데이터가 없습니다.")
    
# 🔍 매칭 오류 디버깅 (점수가 제대로 보이는지 확인)
with st.expander("데이터가 이상한가요? 여기를 클릭해서 전체 데이터 구조를 확인하세요."):
    st.write(df.head(20))
