import streamlit as st
import numpy as np

# 1. 매핑 테이블 및 지능형 검색 엔진
MAPPING_TABLE = {
    "teams": {
        "보스턴": 111, "레드삭스": 111, "볼티모어": 110, "볼티": 110,
        "양키스": 147, "양키": 147, "다저스": 119, "LA": 119
    },
    "players": {
        "디버스": "Rafael Devers", "저지": "Aaron Judge", 
        "소토": "Juan Soto", "카사스": "Triston Casas"
    }
}

def find_exact_name(input_str, category="players"):
    source = MAPPING_TABLE.get(category, {})
    for key, val in source.items():
        if input_str in key:
            return val
    return input_str

# 2. 메인 인터페이스
st.set_page_config(layout="wide")
st.title("⚾ MLB AI 지능형 선수/팀 분석기 v40.0")

# 입력 파트
raw_name = st.text_input("분석할 선수 이름 입력 (예: '디버')", "")

if st.button("선수 데이터 분석"):
    if raw_name:
        accurate_name = find_exact_name(raw_name, "players")
        
        with st.spinner(f"'{accurate_name}'의 데이터 분석 중..."):
            # 가상 스탯 산출 (실제 데이터 호출로 대체 가능)
            np.random.seed(len(accurate_name))
            stats = {
                "wOBA": round(np.random.uniform(0.300, 0.450), 3),
                "Whiff%": f"{round(np.random.uniform(15, 30), 1)}%"
            }
            
            st.success(f"인식 결과: {accurate_name}")
            st.subheader("📊 핵심 성적 지표")
            st.json(stats)
    else:
        st.warning("선수 이름을 입력해주세요.")
