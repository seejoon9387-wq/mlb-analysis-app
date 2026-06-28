import streamlit as st
import pandas as pd
import requests
import io

FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"
FILE_ID_PLAYER = "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"

def verify_file(fid):
    url = f"https://drive.google.com/uc?export=download&id={fid}"
    res = requests.get(url)
    
    # 디버깅용: 응답 상태 확인
    if res.status_code != 200:
        return None, f"HTTP 에러: {res.status_code}"
    if b"<!doctype html>" in res.content:
        return None, "HTML 페이지가 반환됨 (파일 권한 혹은 바이러스 스캔 경고)"
    
    try:
        df = pd.read_csv(io.BytesIO(res.content))
        return df, "성공"
    except Exception as e:
        return None, f"CSV 읽기 실패: {str(e)}"

# 실행 및 진단
st.title("데이터 로드 진단기")

# 진단 실행
for name, fid in [("경기 기록", FILE_ID_GAME), ("선수 기록", FILE_ID_PLAYER)]:
    df, status = verify_file(fid)
    if df is not None:
        st.success(f"{name} 로드 성공! ({len(df)}행)")
    else:
        st.error(f"{name} 로드 실패: {status}")
