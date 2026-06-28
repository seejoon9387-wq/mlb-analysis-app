import streamlit as st
import pandas as pd
import requests
import io

# 페이지 설정
st.set_page_config(page_title="MLB 통합 조회 시스템", layout="wide")
st.title("⚾ MLB 2024-2026 통합 경기 조회 시스템")

# 파일 아이디 리스트 (여기에 사용하실 최신 파일 아이디를 넣어주세요)
FILE_IDS = ["1HoUl7WmX2YuLww3yNg6O09IB0kwOJEtN", "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"]

@st.cache_data
def load_and_clean_data(ids):
    all_dfs = []
    for fid in ids:
        # 'confirm=t' 옵션을 통해 바이러스 스캔 경고 우회
        url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
        try:
            res = requests.get(url)
            # HTML 형태의 오류 페이지인지 확인
            if b"<!doctype html>" in res.content:
                continue
            
            df = pd.read_csv(io.BytesIO(res.content))
            df.columns = [c.strip().lower() for c in df.columns]
            
            # 날짜 컬럼 보정
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                all_dfs.append(df)
        except Exception as e:
            st.error(f"파일 {fid} 로드 중 오류: {e}")
    
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

# 1. 데이터 로드 및 상태 표시
with st.spinner('데이터 동기화 중...'):
    df = load_and_clean_data(FILE_IDS)

if not df.empty:
    # 데이터 범위 자동 계산
    min_d, max_d = df['date'].min().date(), df['date'].max().date()
    st.info(f"현재 보유 데이터 범위: {min_d} ~ {max_d}")
    
    # 2. 달력 UI
    st.subheader("🗓️ 경기 결과 조회")
    selected_date = st.date_input("조회할 날짜를 선택하세요:", value=max_d)
    
    # 3. 필터링 및 출력
    match_data = df[df['date'].dt.date == selected_date]
    
    if not match_data.empty:
        st.success(f"{selected_date} 경기 결과 ({len(match_data)}건)")
        st.dataframe(match_data, use_container_width=True)
    else:
        st.warning(f"{selected_date}에 해당하는 데이터가 없습니다. 위 데이터 범위를 확인해주세요.")
        
    # 데이터 미리보기 (디버깅용)
    with st.expander("데이터 샘플 확인하기"):
        st.write(df.head())
else:
    st.error("데이터를 가져올 수 없습니다. 파일이 비어있거나 공유 설정이 '링크가 있는 모든 사용자'로 되어있는지 확인하세요.")
