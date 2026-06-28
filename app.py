import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(layout="wide")
st.title("⚾ MLB 데이터 조회 시스템 (수정판)")

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
            st.error(f"파일 {fid} 로드 에러: {e}")
    
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

df = load_and_clean_data(FILE_IDS)

if not df.empty:
    # 🗓️ 달력 선택
    selected_date = st.date_input("조회할 날짜를 선택하세요:")
    # 선택된 날짜를 문자열(예: '2026-06-28')로 변환
    target_date_str = str(selected_date)
    
    # 데이터의 date 컬럼도 문자열로 변환하여 비교 (형식 차이 무시)
    df['date_str'] = df['date'].astype(str)
    
    # 날짜 필터링
    result = df[df['date_str'].str.contains(target_date_str)]
    
    if not result.empty:
        st.write(f"### {target_date_str} 경기 결과")
        st.dataframe(result, use_container_width=True)
    else:
        st.warning(f"{target_date_str}에 일치하는 데이터가 없습니다.")
        st.write("샘플 데이터 확인:")
        st.write(df['date'].head(5).tolist()) # 어떤 형식으로 저장되어 있는지 확인
else:
    st.warning("데이터 로드 실패")
