import streamlit as st
import pandas as pd
import requests
import io

def load_data_from_drive(file_ids):
    all_dfs = []
    for fid in file_ids:
        url = f"https://drive.google.com/uc?id={fid}"
        try:
            res = requests.get(url)
            df = pd.read_csv(io.BytesIO(res.content))
            
            # --- [핵심 수정: 컬럼명 자동 보정] ---
            # 컬럼 이름들을 소문자로 바꾸고 공백 제거 (Date, date, 날짜 등 모두 대응)
            df.columns = [c.strip().lower() for c in df.columns]
            
            # 만약 'date'라는 이름이 없다면, 첫 번째 컬럼을 'date'로 강제 지정
            if 'date' not in df.columns:
                df.rename(columns={df.columns[0]: 'date'}, inplace=True)
            
            # 날짜 형식 변환 (에러 발생 시 무시하고 데이터 그대로 유지)
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            all_dfs.append(df)
        except Exception as e:
            st.error(f"파일 ID {fid} 처리 중 오류: {e}")
    
    return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()

# ... (이하 달력 UI 구성은 동일)
