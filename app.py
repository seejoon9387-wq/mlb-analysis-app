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
        df = pd.read_csv(io.BytesIO(res.content))
        # 1. 컬럼명을 소문자로 통일하고 앞뒤 공백 제거
        df.columns = [c.strip().lower() for c in df.columns]
        return df

    df_game = get_df(FILE_ID_GAME)
    df_player = get_df(FILE_ID_PLAYER)
    
    # 2. 날짜 컬럼 자동 찾기 (date 또는 날짜 관련 이름이 없으면 0번 컬럼 사용)
    def clean_date_col(df):
        date_col = next((c for c in df.columns if 'date' in c), df.columns[0])
        df = df.rename(columns={date_col: 'date'})
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        return df

    df_game = clean_date_col(df_game)
    df_player = clean_date_col(df_player)
    
    # 3. 데이터 병합 (날짜 기준)
    # 선수기록(player)에 경기기록(game)을 붙입니다.
    merged_df = pd.merge(df_player, df_game, on='date', how='left')
    
    return merged_df

# 로드 실행
try:
    df = load_and_merge_stats()
    st.dataframe(df.head()) # 데이터가 잘 합쳐졌는지 확인
    st.write("컬럼 목록:", list(df.columns))
except Exception as e:
    st.error(f"오류 발생: {e}")
