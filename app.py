import streamlit as st
import statsapi
import pandas as pd
import datetime
import os

DATA_FILE = "backtest_log.csv"

# 데이터 저장 로직
def save_log(team_name, predicted_score):
    new_data = pd.DataFrame([{'date': datetime.date.today(), 'team': team_name, 'prediction': predicted_score}])
    if not os.path.exists(DATA_FILE):
        new_data.to_csv(DATA_FILE, index=False)
    else:
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)

# 데이터 불러오기 로직 (문자열 반환 금지, 항상 DataFrame 반환)
def get_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except:
            return pd.DataFrame(columns=['date', 'team', 'prediction'])
    return pd.DataFrame(columns=['date', 'team', 'prediction'])

st.title("⚾ MLB AI 마스터 엔진 v57.0")

team_name = st.text_input("팀 입력", "보스턴")

if st.button("분석 시작 및 기록 저장"):
    save_log(team_name, 0.320)
    st.success("데이터가 기록되었습니다!")
    st.rerun()

st.subheader("저장된 기록")
# 항상 DataFrame을 넘기므로 에러가 발생하지 않습니다.
data = get_data()
if data.empty:
    st.write("현재 저장된 기록이 없습니다.")
else:
    st.table(data)
