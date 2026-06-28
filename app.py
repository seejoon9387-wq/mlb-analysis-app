import streamlit as st
import pandas as pd
import requests
import io

FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"

@st.cache_data
def load_game_data(fid):
    url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
    res = requests.get(url)
    df = pd.read_csv(io.BytesIO(res.content))
    df.columns = [c.strip().lower() for c in df.columns]
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

st.set_page_config(layout="wide")
st.title("⚾ MLB 2024-2026 경기 결과 시스템")

df = load_game_data(FILE_ID_GAME)

if not df.empty:
    # 달력 위치 강제 확보
    st.markdown("### 🗓️ 조회할 날짜를 선택하세요")
    
    # 두 가지 방식을 동시에 제공하여 달력 문제 우회
    col1, col2 = st.columns(2)
    
    with col1:
        # 달력 UI
        selected_date = st.date_input("달력에서 선택:", value=df['date'].max())
    
    with col2:
        # 텍스트 직접 입력 방식 (달력이 안 보일 때 대비)
        manual_date = st.text_input("날짜 직접 입력 (YYYY-MM-DD):", value=str(df['date'].max().date()))

    # 날짜 필터링 로직
    try:
        final_date = pd.to_datetime(manual_date).date()
    except:
        final_date = selected_date

    match_data = df[df['date'].dt.date == final_date]
    
    if not match_data.empty:
        st.write(f"### {final_date} 경기 결과")
        st.dataframe(match_data, use_container_width=True)
    else:
        st.warning(f"{final_date}에는 경기가 없습니다.")
else:
    st.error("데이터 로드 실패")
