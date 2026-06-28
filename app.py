# 버전: v68.0
# 목적: 클라우드 환경에서 안전한 데이터 수집 및 시각화
import streamlit as st
import pandas as pd
from pybaseball import statcast
import datetime

st.title("⚾ MLB AI 마스터 엔진 v68.0 (데이터 수집 센터)")

# 수집할 연도 선택
year = st.selectbox("수집할 연도 선택", [2024, 2025, 2026])

if st.button(f"{year}년 데이터 수집 시작"):
    with st.spinner(f"{year}년 데이터를 불러오는 중입니다..."):
        try:
            # 4월부터 9월까지 1달 단위로 수집 (메모리 초과 방지)
            all_data = []
            for month in range(4, 10):
                start = f"{year}-{month:02d}-01"
                end = f"{year}-{month:02d}-28"
                
                # 수집 실행
                monthly_data = statcast(start_dt=start, end_dt=end)
                all_data.append(monthly_data)
                st.write(f"✅ {month}월 데이터 {len(monthly_data)}건 수집 완료")
            
            # 병합
            final_df = pd.concat(all_data)
            st.success(f"총 {len(final_df)}건의 데이터 수집 완료!")
            
            # 결과 미리보기
            st.dataframe(final_df.head(10))
            
            # CSV 다운로드 버튼 제공 (클라우드에서는 이게 제일 안전함)
            csv = final_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="전체 데이터 CSV로 저장하기",
                data=csv,
                file_name=f"mlb_data_{year}.csv",
                mime='text/csv',
            )
        except Exception as e:
            st.error(f"수집 중 오류 발생: {e}")

st.info("💡 팁: 수집된 데이터는 'CSV로 저장' 버튼을 통해 PC로 다운로드하세요. 나중에 다시 업로드하여 분석할 수 있습니다.")
