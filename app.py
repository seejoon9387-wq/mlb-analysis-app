import streamlit as st
import pandas as pd
import requests
import io

FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"  # 경기기록
FILE_ID_PLAYER = "1iFelqEtUV-SQqnMeAuEN_XdEMjyuU9jH" # 선수기록

@st.cache_data
def load_and_merge_stats():
    # 데이터 로드
    def get_df(fid):
        url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
        res = requests.get(url)
        df = pd.read_csv(io.BytesIO(res.content))
        df.columns = [c.strip().lower() for c in df.columns]
        return df

    df_game = get_df(FILE_ID_GAME)
    df_player = get_df(FILE_ID_PLAYER)
    
    # 1. 날짜를 datetime으로 통일
    df_game['date'] = pd.to_datetime(df_game['date'])
    df_player['date'] = pd.to_datetime(df_player['date'])
    
    # 2. 'date'와 'team' 컬럼을 기준으로 합침 (Merge)
    # 선수 기록에 'team' 컬럼이 있다고 가정합니다.
    merged_df = pd.merge(df_player, df_game, on=['date'], how='left')
    
    return merged_df

# UI 처리
df = load_and_merge_stats()

# 이후 달력 필터링 코드 (이전과 동일)
