# 버전: v74.0
# 목적: 파일 유무 확인 후 안전하게 병합
import pandas as pd
import glob
import streamlit as st

def clean_and_merge_data():
    # 현재 폴더에 있는 모든 mlb_*.csv 파일 찾기
    all_files = glob.glob("mlb_*.csv")
    
    # 파일이 하나라도 있는지 확인
    if not all_files:
        st.error("❌ 병합할 파일이 없습니다! 다운로드받은 CSV 파일들을 같은 폴더에 업로드했는지 확인하세요.")
        return None
    
    st.write(f"📂 발견된 파일 수: {len(all_files)}개")
    
    df_list = [pd.read_csv(f) for f in all_files]
    full_df = pd.concat(df_list, ignore_index=True)
    
    # 중복 제거 (데이터에 pitch_id가 반드시 있어야 함)
    if 'pitch_id' in full_df.columns:
        clean_df = full_df.drop_duplicates(subset=['pitch_id'])
    else:
        clean_df = full_df.drop_duplicates()
        
    st.success(f"✅ 중복 제거 완료! 총 데이터: {len(clean_df)}건")
    return clean_df

# Streamlit UI에서 실행
if st.button("데이터 병합 시작"):
    final_data = clean_and_merge_data()
    if final_data is not None:
        st.download_button("최종 데이터 저장", final_data.to_csv(index=False), "final_data.csv")
