import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(layout="wide")
st.title("⚾ MLB 데이터 조회 테스트")

FILE_IDS = ["1HoUl7WmX2YuLww3yNg6O09IB0kwOJEtN", "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"]

# 데이터 로드 함수
def load_all_data(ids):
    data_frames = []
    for fid in ids:
        url = f"https://drive.google.com/uc?id={fid}"
        try:
            res = requests.get(url)
            df = pd.read_csv(io.BytesIO(res.content))
            df.columns = [c.strip().lower() for c in df.columns] # 컬럼명 보정
            data_frames.append(df)
            st.write(f"파일 {fid} 로드 성공! (컬럼: {list(df.columns)})") # 로드 성공 확인용
        except Exception as e:
            st.error(f"파일 {fid} 로드 중 에러: {e}")
    return pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()

# 데이터 가져오기
df = load_all_data(FILE_IDS)

if not df.empty:
    st.write(f"데이터 총 개수: {len(df)}")
    st.dataframe(df.head()) # 데이터가 제대로 들어왔는지 확인
else:
    st.warning("데이터가 비어있습니다. 구글 드라이브 공유 설정을 확인하세요.")
