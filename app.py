import streamlit as st
import pandas as pd
import requests
import io

FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"
FILE_ID_PLAYER = "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH"

@st.cache_data
def load_and_merge_stats():
    def get_df(fid):
        url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
        res = requests.get(url)
        
        # 1. HTML 페이지인지 확인하고, 그렇다면 진짜 다운로드 링크로 다시 시도
        if b"<!doctype html>" in res.content:
            # HTML 경고 페이지라면 파일 내용을 아예 무시하고 빈 데이터프레임 반환
            return pd.DataFrame()
        
        df = pd.read_csv(io.BytesIO(res.content))
        df.columns = [c.strip().lower() for c in df.columns]
        return df

    df_game = get_df(FILE_ID_GAME)
    df_player = get_df(FILE_ID_PLAYER)
    
    # 2. 로드 실패(빈 데이터) 확인
    if df_game.empty or df_player.empty:
        return None, "데이터 중 하나가 로드되지 않았습니다. 파일 공유 설정을 다시 확인하세요."

    # 3. 날짜 컬럼 보정 및 병합
    df_game['date'] = pd.to_datetime(df_game['date'], errors='coerce')
    
    # 선수 데이터도 'date' 컬럼이 있는 파일이어야 합니다.
    # 만약 선수 데이터에 date가 없다면 이름 확인이 필요합니다.
    df_player['date'] = pd.to_datetime(df_player['date'], errors='coerce')
    
    merged_df = pd.merge(df_player, df_game, on='date', how='left')
    return merged_df, None

# UI 실행
df, error_msg = load_and_merge_stats()

if error_msg:
    st.error(error_msg)
else:
    st.success("통합 완료!")
    st.dataframe(df.head())
