import streamlit as st
import pandas as pd
import requests
import io

FILE_ID_GAME = "1_xl0LlfH65-K1TAsyH7nUq7ExQB5JTWx"

@st.cache_data
def inspect_data(fid):
    url = f"https://drive.google.com/uc?export=download&confirm=t&id={fid}"
    res = requests.get(url)
    df = pd.read_csv(io.BytesIO(res.content))
    return df

st.title("🔍 데이터 상태 정밀 검사")
df = inspect_data(FILE_ID_GAME)

st.write("### 1. 데이터 전체 컬럼 이름")
st.write(df.columns.tolist())

st.write("### 2. 데이터 미리보기 (상위 10줄)")
st.dataframe(df.head(10))
