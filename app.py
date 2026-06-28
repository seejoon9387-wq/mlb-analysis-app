# 버전: v74.2
# 목적: 사용자가 직접 파일을 업로드하여 브라우저에서 즉시 병합 및 중복 제거
import streamlit as st
import pandas as pd

st.title("⚾ MLB 최종 데이터 통합기 (v74.2)")

# 1. 파일 업로더 생성 (여러 파일 동시 선택 가능)
uploaded_files = st.file_uploader("수집한 모든 CSV 파일들을 여기에 끌어다 놓으세요", accept_multiple_files=True)

if uploaded_files:
    if st.button("병합 및 중복 제거 시작"):
        with st.spinner("데이터를 합치고 중복을 제거하는 중입니다..."):
            try:
                # 2. 모든 파일 읽기
                df_list = [pd.read_csv(f) for f in uploaded_files]
                full_df = pd.concat(df_list, ignore_index=True)
                
                # 3. 중복 제거
                # pitch_id가 있으면 기준으로, 없으면 전체 행 기준으로 제거
                if 'pitch_id' in full_df.columns:
                    clean_df = full_df.drop_duplicates(subset=['pitch_id'])
                else:
                    clean_df = full_df.drop_duplicates()
                
                st.success(f"✅ 완료! 전체 {len(full_df)}건 중 중복을 제거하여 {len(clean_df)}건이 남았습니다.")
                
                # 4. 결과 다운로드
                csv = clean_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="최종 데이터 다운로드 (final_data.csv)",
                    data=csv,
                    file_name="final_mlb_data_2024_2026.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"병합 중 오류가 발생했습니다: {e}")
else:
    st.info("💡 CSV 파일들을 모두 선택해 주세요. 선택된 파일들이 메모리 상에서 즉시 병합됩니다.")
