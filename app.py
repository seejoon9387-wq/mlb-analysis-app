import streamlit as st
import pandas as pd
import statsapi
from datetime import datetime

# --- [한글 변환 딕셔너리] ---
status_map = {
    "Pre-Game": "경기 전",
    "Scheduled": "예정",
    "Final": "종료",
    "In Progress": "진행 중"
}

def get_game_data():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        games = statsapi.schedule(date=today)
        if not games:
            return None
        
        game_list = []
        for game in games:
            # 1. 시간 데이터 확보 (상세 필드인 game_time 대신 raw_time 시도)
            raw_time = game.get('game_time', '시간 미정')
            
            # 2. 상태 한글화
            status_en = game.get('status', 'Scheduled')
            status_ko = status_map.get(status_en, status_en)
            
            game_list.append({
                "날짜": game.get('game_date'),
                "시간": raw_time,
                "원정": game.get('away_name'),
                "원정 선발": game.get('away_probable_pitcher', '미정'),
                "홈": game.get('home_name'),
                "홈 선발": game.get('home_probable_pitcher', '미정'),
                "상태": status_ko
            })
        return pd.DataFrame(game_list)
    except Exception as e:
        return None

def main():
    st.set_page_config(page_title="MLB 경기 분석", layout="wide")
    st.title("⚾ MLB 오늘 경기 일정")
    
    if st.button("경기 정보 새로고침"):
        df = get_game_data()
        if df is not None:
            # st.table 대신 st.dataframe을 사용하면 훨씬 깔끔합니다
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("오늘 경기가 없거나 정보를 불러올 수 없습니다.")

if __name__ == "__main__":
    main()
