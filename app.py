import streamlit as st
import pandas as pd

url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
df = pd.read_csv(url)

st.write("### 1. 데이터 상위 5줄")
st.write(df.head())

st.write("### 2. 데이터 컬럼 정보")
st.write(df.dtypes)
