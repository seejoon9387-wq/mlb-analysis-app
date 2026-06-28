# 버전: v73.0
# 목적: 수집된 CSV 조각들을 합치고 중복 제거
import pandas as pd
import glob

# 1. 다운로드받은 파일들이 있는 폴더에 모두 모아두세요
# 2. 아래 코드를 실행하면 중복이 제거된 하나의 파일이 생성됩니다.
def clean_and_merge_data():
    # 모든 csv 파일 불러오기
    all_files = glob.glob("mlb_*.csv")
    
    # 리스트에 담기
    df_list = [pd.read_csv(f) for f in all_files]
    
    # 하나로 합치기
    full_df = pd.concat(df_list, ignore_index=True)
    
    # 중복 제거 (스탯캐스트 데이터는 'pitch_id'가 고유값입니다)
    # 만약 pitch_id가 없다면 모든 컬럼 기준으로 제거
    clean_df = full_df.drop_duplicates(subset=['pitch_id'])
    
    # 결과 저장
    clean_df.to_csv("final_mlb_data_2024_2026.csv", index=False)
    print(f"중복 제거 전: {len(full_df)}건 -> 제거 후: {len(clean_df)}건")

# 실행
clean_and_merge_data()
