import streamlit as st
import pandas as pd
import requests
import io

# 1. 구글 드라이브에서 데이터 가져오기 (통합)
def load_data_from_drive(file_ids):
    all_dfs = []
    for fid in file_ids:
        url = f"https://drive.google.com/uc?id={fid}"
        try:
            res = requests.get(url)
            df = pd.read_csv(io.BytesIO(res.content))
            # 날짜 컬럼을 datetime 형식으로 변환 (필수)
            df['date'] = pd.to_datetime(df['date'])
            all_dfs.append(df)
        except Exception as e:
            st.error(f"파일 ID {fid} 로드 중 오류 발생: {e}")
    
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

# 2. 대시보드 UI 구성
st.set_page_config(page_title="MLB 경기 달력 조회", layout="wide")
st.title("⚾ MLB 2024-2026 경기 달력 조회")

FILE_IDS = ["1HoUl7WmX2YuLww3yNg6O09IB0kwOJEtN", "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"]

with st.spinner('구글 드라이브에서 경기를 불러오는 중입니다...'):
    df = load_data_from_drive(FILE_IDS)

if not df.empty:
    # 3. 달력 기반 날짜 선택
    st.subheader("🗓️ 날짜를 선택하여 경기 기록 확인")
    selected_date = st.date_input("조회하고 싶은 날짜를 선택하세요:")
    
    # 선택된 날짜 데이터 필터링
    match_data = df[df['date'].dt.date == selected_date]
    
    if not match_data.empty:
        st.success(f"{selected_date}에 총 {len(match_data)}개의 경기가 있습니다.")
        # 표 형태로 결과 출력
        st.dataframe(match_data, use_container_width=True)
    else:
        st.info("선택하신 날짜에 진행된 경기가 없습니다.")
else:
    st.error("데이터를 불러올 수 없습니다. 파일 공유 설정(링크가 있는 모든 사용자)을 확인해주세요.")
