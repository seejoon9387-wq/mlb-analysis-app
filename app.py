import streamlit as st
import pandas as pd
import statsapi
from datetime import datetime
import pytz

# 팀 이름 한글 매핑
team_map = {
    "Washington Nationals": "워싱턴 내셔널스", "Baltimore Orioles": "볼티모어 오리올스",
    "Cincinnati Reds": "신시내티 레즈", "Pittsburgh Pirates": "피츠버그 파이리츠",
    "Texas Rangers": "텍사스 레인저스", "Toronto Blue Jays": "토론토 블루제이스",
    "Houston Astros": "휴스턴 애스트로스", "Detroit Tigers": "디트로이트 타이거즈",
    "Seattle Mariners": "시애틀 매리너스", "Cleveland Guardians": "클리블랜드 가디언스",
    "Arizona Diamondbacks": "애리조나 다이아몬드백스", "Tampa Bay Rays": "탬파베이 레이스",
    "Philadelphia Phillies": "필라델피아 필리스", "New York Mets": "뉴욕 메츠",
    "Colorado Rockies": "콜로라도 로키스", "Minnesota Twins": "미네소타 트윈스",
    "Kansas City Royals": "캔자스시티 로열스", "Chicago White Sox": "시카고 화이트삭스",
    "Chicago Cubs": "시카고 컵스", "Milwaukee Brewers": "밀워키 브루어스",
    "Miami Marlins": "마이애미 말린스", "St. Louis Cardinals": "세인트루이스 카디런스",
    "Athletics": "오클랜드 애슬레틱스", "Los Angeles Angels": "LA 에인절스",
    "Atlanta Braves": "애틀랜타 브레이브스", "San Francisco Giants": "샌프란시스코 자이언츠",
    "Los Angeles Dodgers": "LA 다저스", "San Diego Padres": "샌디에이고 파드리스",
    "New York Yankees": "뉴욕 양키스", "Boston Red Sox": "보스턴 레드삭스"
}

def get_kst_time(iso_time_str):
    """미국 시간을 한국 시간으로 변환하는 함수"""
    try:
        # API 시간 형식(ISO)을 datetime 객체로 변환
        dt = datetime.fromisoformat(iso_time_str.replace('Z', '+00:00'))
        # UTC를 한국 시간(Asia/Seoul)으로 변환
        kst = dt.astimezone(pytz.timezone('Asia/Seoul'))
        return kst.strftime('%m/%d %H:%M')
    except:
        return "시간 미정"

def get_game_data():
    today = datetime.now().strftime('%Y-%m-%d')
    try:
        games = statsapi.schedule(date=today)
        if not games: return None
        
        game_list = []
        for g in games:
            # 시간 데이터 변환 (game_datetime 필드 사용)
            kst_time = get_kst_time(g.get('game_datetime')) if g.get('game_datetime') else "시간 미정"
            
            game_list.append({
                "일시": kst_time,
                "원정": team_map.get(g.get('away_name'), g.get('away_name')),
                "원정 선발": g.get('away_probable_pitcher', '미정'),
                "홈": team_map.get(g.get('home_name'), g.get('home_name')),
                "홈 선발": g.get('home_probable_pitcher', '미정'),
                "상태": "경기 전" if g.get('status') in ['Pre-Game', 'Scheduled'] else g.get('status')
            })
        return pd.DataFrame(game_list)
    except Exception:
        return None

# 메인 UI
st.set_page_config(layout="wide")
st.title("⚾ MLB 오늘 경기 일정 (한국 시간 기준)")

if st.button("데이터 불러오기"):
    df = get_game_data()
    if df is not None:
        st.dataframe(df, use_container_width=True)
    else:
        st.write("오늘 일정이 없습니다.")
