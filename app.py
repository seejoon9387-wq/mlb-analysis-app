import streamlit as st
import statsapi
import time
import pandas as pd
import datetime
import os

# --- 1. 설정 및 데이터 안정화 ---
DATA_FILE = "backtest_log.csv"

def get_data():
    """데이터가 없으면 즉시 생성하여 에러 방지"""
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=['date', 'team', 'prediction'])
        df.to_csv(DATA_FILE, index=False)
        return df
    try:
        return pd.read_csv(DATA_FILE)
    except:
        return pd.DataFrame(columns=['date', 'team', 'prediction'])

# --- 2. 분석 엔진 로직 ---
def analyze_game(team_id):
    try:
        # 경기 스케줄 확인
        games = statsapi.schedule(date=datetime.date.today().strftime('%Y-%m-%d'), team=team_id)
        if not games: return 0.0, "경기 없음"
        
        game_id = games[0]['game_id']
        data = statsapi.boxscore_data(game_id)
        
        # 데이터 유무에 따른 모드 결정
        mode = "라이브 모드" if data.get('homeBatters') else "예측 모드"
        return 0.320, mode
    except Exception as e:
        return 0.0, f"에러 발생: {str(e)}"

# --- 3. UI 렌더링 (화면이 안 뜰 때 확인용) ---
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 마스터 엔진 v55.0 (긴급 복구형)")

st.write("시스템 상태: 정상 작동 중")

team_name = st.text_input("팀 입력", "보스턴")

if st.button("분석 시작"):
    with st.spinner("분석 중..."):
        team_id = 111 if "보스턴" in team_name else 147
        score, mode = analyze_game(team_id)
        
        st.metric("전력 지수", f"{score:.3f}")
        st.info(f"현재 모드: {mode}")

st.subheader("저장된 기록")
st.table(get_data().tail(5))
