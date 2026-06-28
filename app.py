# 버전: v71.0
# 목적: 클라우드 메모리 오류 방지를 위한 월 단위 스트리밍 수집
import streamlit as st
import pandas as pd
from pybaseball import statcast

st.title("⚾ v71.0 정규시즌 스트리밍 수집기")

year = st.selectbox("수집할 연도 선택", [2024, 2025, 2026])

if st.button("수집 시작 (월 단위 저장)"):
    full_data = []
    # 3월~9월까지 한 달씩 처리
    for month in range(3, 10):
        try:
            st.write(f"⏳ {month}월 데이터 수집 중...")
            # 1일~28일로 짧게 끊어서 호출 (데이터 손실 방지)
            data = statcast(start_dt=f"{year}-{month:02d}-01", end_dt=f"{year}-{month:02d}-28")
            
            # 수집 즉시 결과 확인 및 리스트 추가
            st.write(f"✅ 완료: {len(data)}건")
            full_data.append(data)
            
            # 여기서 메모리 관리: 필요하다면 중간 데이터는 삭제
        except Exception as e:
            st.error(f"{month}월 오류: {e}")
            
    if full_data:
        final_df = pd.concat(full_data)
        st.success(f"총 {len(final_df)}건 수집 완료!")
        
        # 파일 저장 후 링크 제공
        csv = final_df.to_csv(index=False).encode('utf-8')
        st.download_button("데이터 다운로드", csv, f"mlb_{year}_data.csv", "text/csv")
