import streamlit as st
import statsapi
import pandas as pd
import datetime
import os

DATA_FILE = "backtest_log.csv"

# 데이터 저장 로직 수정 (파일이 없으면 헤더 생성, 있으면 추가)
def save_log(team_name, predicted_score):
    new_data = pd.DataFrame([{'date': datetime.date.today(), 'team': team_name, 'prediction': predicted_score}])
    if not os.path.exists(DATA_FILE):
        new_data.to_csv(DATA_FILE, index=False)
    else:
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)

def get_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        return df if not df.empty else "데이터가 비어있습니다."
    return "파일이 아직 생성되지 않았습니다."

st.title("⚾ MLB AI 마스터 엔진 v56.0")

team_name = st.text_input("팀 입력", "보스턴")

if st.button("분석 시작 및 기록 저장"):
    # 강제로 데이터 기록
    save_log(team_name, 0.320)
    st.success("데이터가 기록되었습니다! 아래 표를 확인하세요.")
    st.rerun() # 데이터를 저장하자마자 화면 새로고침

st.subheader("저장된 기록")
data = get_data()
st.table(data)
