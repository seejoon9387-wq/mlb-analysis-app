import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(layout="wide")
st.title("⚾ MLB 통합 경기 조회 시스템")

FILE_IDS = ["1HoUl7WmX2YuLww3yNg6O09IB0kwOJEtN", "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"]

@st.cache_data
def load_and_clean_data(ids):
    all_dfs = []
    for fid in ids:
        url = f"https://drive.google.com/uc?id={fid}"
        try:
            res = requests.get(url)
            # HTML 코드가 들어오면 데이터프레임 변환 시 에러가 나거나 불필요한 데이터가 됨
            if b"<!doctype html>" in res.content:
                # 다운로드 링크 우회: 'confirm=t' 파라미터 추가하여 바이러스 검사 경고 건너뛰기
                url_bypass = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
                res = requests.get(url_bypass)
            
            df = pd.read_csv(io.BytesIO(res.content))
            df.columns = [c.strip().lower() for c in df.columns]
            
            # 'date' 컬럼만 추출하여 정제
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                all_dfs.append(df)
        except Exception as e:
            st.error(f"파일 {fid} 로드 중 에러: {e}")
            
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

# 데이터 로드
df = load_and_clean_data(FILE_IDS)

if not df.empty:
    st.success(f"데이터 로드 성공! 총 {len(df)}건")
    
    # 🗓️ 달력 UI
    selected_date = st.date_input("조회할 날짜를 선택하세요:")
    
    # 필터링
    result = df[df['date'].dt.date == selected_date]
    
    if not result.empty:
        st.dataframe(result, use_container_width=True)
    else:
        st.info("해당 날짜의 데이터가 없습니다.")
else:
    st.warning("데이터를 읽어올 수 없습니다. 파일 공유 설정을 다시 확인하세요.")
