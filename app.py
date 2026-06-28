import streamlit as st
import statsapi

# 1. 데이터 필드 정밀 진단 엔진
def inspect_game_data(game_id):
    data = statsapi.boxscore_data(game_id)
    player_info = data.get('playerInfo', {})
    
    if not player_info: return False, []
    
    # 첫 번째 선수로 필드 가용성 진단
    first_key = list(player_info.keys())[0]
    hitting_stats = player_info[first_key].get('stats', {}).get('hitting', {})
    
    return len(hitting_stats) > 0, list(hitting_stats.keys())

# 2. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 데이터 인지형 분석기 v49.0")

if st.sidebar.button("오늘 경기 데이터 진단 실행"):
    with st.spinner("경기 스케줄 확인 및 데이터 필드 진단 중..."):
        games = statsapi.schedule(date='2026-06-28', team=111)
        if games:
            game_id = games[0]['game_id']
            ready, fields = inspect_game_data(game_id)
            
            st.success(f"데이터 진단 완료! (Game ID: {game_id})")
            
            if ready:
                st.info("데이터 필드 가용: 분석 엔진을 가동합니다.")
                st.write(f"추적 가능 지표: {', '.join(fields)}")
            else:
                st.warning("데이터가 준비 중입니다. 예상 라인업 모드로 전환합니다.")
        else:
            st.error("오늘 보스턴 경기 데이터가 없습니다.")
