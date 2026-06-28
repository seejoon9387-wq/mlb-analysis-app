import streamlit as st
import statsapi

# [이미 완성된 함수들 생략: analyze_day_night_impact, get_lineup_live_safe 등]
# 이 섹션에는 기존에 정의한 모든 유틸리티 함수가 포함됩니다.

st.set_page_config(layout="wide")
st.title("⚾ MLB AI 오늘의 매치업 실시간 분석기 v46.0")

if st.sidebar.button("오늘(2026-06-28) 보스턴 분석 가동"):
    with st.spinner("라이브 데이터 동기화 및 환경 보정 분석 중..."):
        # 1. 데이터 추출 및 상태 파악
        team_id = 111
        games = statsapi.schedule(date='2026-06-28', team=team_id)
        
        if not games:
            st.error("오늘 예정된 경기가 없습니다.")
        else:
            game_info = games[0]
            is_home = (game_info['home_id'] == team_id)
            is_day = True # 현지 시간대 반영
            
            # 2. 보정된 분석 실행
            lineup = get_lineup_live_safe(team_id)
            starter_id = game_info['away_id'] if is_home else game_info['home_id']
            
            final_power, comment = analyze_day_night_impact(lineup, starter_id, is_day)
            
            # 3. 결과 리포팅
            st.subheader(f"📊 보스턴 통합 전력 지수: {final_power:.3f}")
            st.info(f"AI 심층 분석: {comment}")
            
            st.success("오늘의 모든 환경 보정 분석이 완료되었습니다.")
