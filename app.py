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
            # 시간 데이터 추출 및 한국어 포맷팅
            raw_time = game.get('game_time', '')
            # 데이터가 있으면 시간만 추출 (예: "7:05 PM ET")
            display_time = raw_time if raw_time else "시간 미정"
            
            game_list.append({
                "경기 ID": game.get('game_id'),
                "날짜": game.get('game_date'),
                "경기 시간": display_time,
                "원정팀": game.get('away_name'),
                "원정 선발": game.get('away_probable_pitcher', '미정'),
                "홈팀": game.get('home_name'),
                "홈 선발": game.get('home_probable_pitcher', '미정'),
                "상태": game.get('status')
            })
        return pd.DataFrame(game_list)
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

# --- [메인 인터페이스] ---
def main():
    st.set_page_config(page_title="MLB 상세 경기 분석 엔진", layout="wide")
    st.title("⚾ MLB 상세 경기 분석 엔진 (v24.1)")
    
    # 표의 헤더를 한글로 강제 지정
    if st.button("오늘의 경기 정보 불러오기"):
        with st.spinner("데이터를 가져오는 중입니다..."):
            df = get_game_data()
            if df is not None:
                # 데이터프레임 컬럼명을 한글로 고정
                df.columns = ["경기 ID", "날짜", "경기 시간", "원정팀", "원정 선발", "홈팀", "홈 선발", "상태"]
                st.table(df)
            else:
                st.warning("오늘 진행되는 경기가 없거나 정보를 가져올 수 없습니다.")

if __name__ == "__main__":
    main()
