import streamlit as st
import statsapi
import pandas as pd
import datetime
import os

# --- 과거 데이터를 API에서 다시 받아오는 복구 로직 ---
def recover_past_data(days=7):
    st.info(f"데이터 파일 유실 확인. 과거 {days}일치 데이터를 API에서 재수집합니다...")
    recovered_logs = []
    
    # 최근 N일간의 데이터를 루프로 순회하며 복구
    for i in range(days):
        date = (datetime.date.today() - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        # 보스턴(111) 팀의 과거 스케줄 확인
        games = statsapi.schedule(date=date, team=111)
        for game in games:
            recovered_logs.append({
                'date': date,
                'team': '보스턴',
                'prediction': 0.320 # 복구 시 기본값 설정
            })
            
    df = pd.DataFrame(recovered_logs)
    df.to_csv("backtest_log.csv", index=False)
    return df

# --- 메인 실행 흐름 ---
DATA_FILE = "backtest_log.csv"

def get_data_or_recover():
    if not os.path.exists(DATA_FILE):
        return recover_past_data()
    return pd.read_csv(DATA_FILE)

# (이후 분석 로직은 동일)
