import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(layout="wide")
st.title("⚾ MLB 데이터 조회 시스템")

FILE_IDS = ["1HoUl7WmX2YuLww3yNg6O09IB0kwOJEtN", "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"]

@st.cache_data
def load_and_clean_data(ids):
    all_dfs = []
    for fid in ids:
        url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
        try:
            res = requests.get(url)
            df = pd.read_csv(io.BytesIO(res.content))
            df.columns = [c.strip().lower() for c in df.columns]
            all_dfs.append(df)
        except Exception as e:
            st.error(f"로드 에러: {e}")
    
    combined_df = pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()
    # 날짜 컬럼을 날짜 형식으로 변환
    combined_df['date'] = pd.to_datetime(combined_df['date'])
    return combined_df

df = load_and_clean_data(FILE_IDS)

if not df.empty:
    # 데이터 범위 안내
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    st.write(f"데이터 범위: {min_date} ~ {max_date}")
    
    # 달력
    selected_date = st.date_input("조회할 날짜를 선택하세요:", value=max_date)
    
    # 필터링 (datetime 형식 비교)
    result = df[df['date'].dt.date == selected_date]
    
    if not result.empty:
        st.write(f"### {selected_date} 경기 결과")
        st.dataframe(result, use_container_width=True)
    else:
        st.warning(f"{selected_date}에 해당하는 데이터가 없습니다. 위 범위 내의 날짜를 선택했는지 확인해주세요.")
else:
    st.error("데이터가 비어있습니다.")
