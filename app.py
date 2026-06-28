import streamlit as st
import pandas as pd
import statsapi
from datetime import datetime

# --- [데이터 처리 엔진] ---
def get_game_data():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        games = statsapi.schedule(date=today)
        if not games:
            return None
        
        game_list = []
        for game in games:
            # 선발 투수 정보 가져오기 (없으면 '미정'으로 표시)
            away_pitcher = game.get('away_probable_pitcher', '미정')
            home_pitcher = game.get('home_probable_pitcher', '미정')
            
            game_list.append({
                "경기 ID": game.get('game_id'),
                "경기 시간": game.get('game_time'),
                "원정팀": game.get('away_name'),
                "원정 선발": away_pitcher,
                "홈팀": game.get('home_name'),
                "홈 선발": home_pitcher,
                "상태": game.get('status')
            })
        return pd.DataFrame(game_list)
    except Exception as e:
        return None

# --- [메인 인터페이스] ---
def main():
    st.set_page_config(page_title="MLB 분석 엔진", layout="wide")
    st.title("⚾ MLB 상세 경기 분석 엔진")
    
    if st.button("오늘의 경기 및 선발 투수 정보 불러오기"):
        with st.spinner("MLB 데이터를 가져오는 중..."):
            df = get_game_data()
            if df is not None:
                # 표 전체 출력
                st.table(df)
            else:
                st.warning("오늘 진행되는 경기가 없습니다.")

if __name__ == "__main__":
    main()
