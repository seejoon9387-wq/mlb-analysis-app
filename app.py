import streamlit as st
import pandas as pd
import requests
from datetime import datetime

@st.cache_data
def get_master_data():
    url = 'https://drive.google.com/uc?export=download&id=1ImEBCjIFN-0K0plfLaQvTcJhhEVHV6DY&confirm=t'
    df = pd.read_csv(url)
    
    # 💡 [진단] 컬럼명을 확인하여 'date'로 간주할 항목을 찾습니다.
    st.write("---")
    st.write("현재 데이터셋 컬럼 확인:", list(df.columns))
    
    # 만약 'date'라는 컬럼이 없으면, 첫 번째 컬럼을 날짜로 간주하도록 보정
    if 'date' not in df.columns:
        # 첫 번째 컬럼을 'date'로 이름 변경 (가장 흔한 케이스)
        df = df.rename(columns={df.columns[0]: 'date'})
        st.warning(f"데이터에 'date' 컬럼이 없어 첫 번째 컬럼 '{df.columns[0]}'을 날짜로 지정했습니다.")
    
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    return df

@st.cache_data
def get_live_schedule(target_date):
    url = f"https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date={target_date}&hydrate=linescore"
    try:
        response = requests.get(url).json()
        games = response['dates'][0]['games']
        data = []
        for g in games:
            data.append({
                "date": target_date,
                "home": g['teams']['home']['team']['name'],
                "away": g['teams']['away']['team']['name']
            })
        return pd.DataFrame(data)
    except: return pd.DataFrame()

# 메인 로직
st.title("⚾ 데이터 매칭 조회")
selected_date = st.date_input("날짜 선택:", datetime.now())

if st.button("데이터 매칭 실행"):
    try:
        master_df = get_master_data()
        live_df = get_live_schedule(selected_date.strftime('%Y-%m-%d'))
        
        if not live_df.empty:
            # 병합 시도
            merged = pd.merge(live_df, master_df, on=['date'], how='inner')
            st.table(merged)
        else:
            st.warning("선택한 날짜에 실시간 데이터가 없습니다.")
    except Exception as e:
        st.error(f"데이터 처리 중 에러 발생: {e}")
