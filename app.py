import streamlit as st
import pandas as pd
import statsapi
import logging
from datetime import datetime

# --- [영역 1: 실시간 데이터 엔진 (누적)] ---
def get_todays_game_info():
    try:
        # 오늘 날짜 기준 경기 일정 호출
        today = datetime.now().strftime('%Y-%m-%d')
        schedule = statsapi.schedule(date=today)
        
        # 데이터를 보기 좋게 DataFrame으로 변환
        df = pd.DataFrame(schedule)
        if not df.empty:
            # 필요한 핵심 컬럼만 추출
            cols = ['game_id', 'game_date', 'away_name', 'home_name', 'status']
            return df[cols]
        else:
            return None
    except Exception as e:
        logging.error(f"실시간 정보 로드 실패: {e}")
        return None

# --- [영역 2: 메인 엔진 (누적)] ---
def main():
    st.title("⚾ MLB 마스터 엔진 (v24.0 - 실시간 테스트)")
    
    st.sidebar.header("엔진 테스트 메뉴")
    menu = st.sidebar.radio("작업 선택", ["실시간 경기 정보", "통합 데이터 분석"])
    
    if menu == "실시간 경기 정보":
        st.subheader(f"오늘 ({datetime.now().strftime('%Y-%m-%d')}) MLB 경기 일정")
        if st.button("실시간 데이터 불러오기"):
            with st.spinner("데이터 수집 중..."):
                game_data = get_todays_game_info()
                
                if game_data is not None:
                    st.success("데이터 호출 성공!")
                    st.dataframe(game_data)
                else:
                    st.warning("오늘 진행 중인 경기가 없거나 데이터를 불러올 수 없습니다.")
                    
    elif menu == "통합 데이터 분석":
        st.write("기존 CSV 분석 엔진이 통합되어 있습니다.")
        # 추후 여기에 기존 CSV 분석 로직 추가

if __name__ == "__main__":
    main()
