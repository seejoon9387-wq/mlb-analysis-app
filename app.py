# 버전: v3.6
# 패치 내용: 데이터 정합성 검증 모드 추가 (실시간 vs 과거 데이터 매칭 테스트)
import streamlit as st
import pandas as pd

# ... (앞서 작성한 load_drive_csv 및 get_mlb_schedule 함수 유지)

if menu == "학습 데이터셋 관리":
    st.subheader("데이터 정합성 테스트 모드")
    if st.button("데이터 매칭 최적화 테스트"):
        with st.spinner('실시간 데이터와 과거 DB를 비교하는 중...'):
            # 1. API 데이터 (실시간)
            api_df = pd.DataFrame(get_mlb_schedule())
            # 2. CSV 데이터 (과거)
            csv_df = load_drive_csv("1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY") # mlb_data_integrated
            
            # 3. 매칭 검증
            api_teams = set(api_df['홈팀'].unique()) | set(api_df['원정팀'].unique())
            csv_teams = set(csv_df['team'].unique())
            
            missing = api_teams - csv_teams
            if not missing:
                st.success("✅ 모든 팀 데이터 매칭 완료!")
            else:
                st.warning(f"⚠️ 매칭되지 않은 팀 발견: {missing}")
                st.write("CSV 내의 팀명과 API 팀명 표기를 일치시켜야 합니다.")
