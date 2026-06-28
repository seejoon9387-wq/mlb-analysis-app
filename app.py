import streamlit as st
import pandas as pd
import statsapi
import os
from datetime import datetime

# --- [데이터 처리 엔진] ---
def get_game_data():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        games = statsapi.schedule(date=today)
        if not games:
            return None
        
        # 데이터를 표 형식(DataFrame)으로 변환
        game_list = []
        for game in games:
            game_list.append({
                "경기 ID": game.get('game_id'),
                "원정팀": game.get('away_name'),
                "홈팀": game.get('home_name'),
                "상태": game.get('status'),
                "경기 시간": game.get('game_time')
            })
        return pd.DataFrame(game_list)
    except Exception as e:
        return None

# --- [메인 인터페이스] ---
def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 마스터 엔진 (v24.0)")
    
    menu = st.sidebar.selectbox("메뉴", ["실시간 경기 정보", "통합 분석 데이터"])
    
    if menu == "실시간 경기 정보":
        st.subheader(f"오늘 ({datetime.now().strftime('%Y-%m-%d')}) MLB 경기 현황")
        if st.button("실시간 데이터 불러오기"):
            with st.spinner("데이터를 가져오는 중입니다..."):
                df = get_game_data()
                if df is not None:
                    st.success("데이터 호출 성공!")
                    st.table(df) # 데이터를 표 형태로 출력
                else:
                    st.warning("오늘 진행 중인 경기가 없거나 정보를 가져올 수 없습니다.")

    elif menu == "통합 분석 데이터":
        st.write("통합 분석 데이터 모듈입니다.")
        # 추후 여기에 추가 로직을 넣습니다.

if __name__ == "__main__":
    main()
