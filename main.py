import streamlit as st
import pandas as pd

# 페이지 기본 설정
st.set_page_config(page_title="글로벌 MBTI 분석 대시보드", layout="wide", initial_sidebar_state="expanded")

# 제목 및 학술적 배경 설명
st.title("🌍 글로벌 MBTI 성향 분석 대시보드")
st.markdown("""
본 대시보드는 전 세계 다양한 국가의 16가지 MBTI 성격 유형 분포 데이터를 탐색하기 위해 개발되었습니다. 
            
**교차 문화 심리학(Cross-Cultural Psychology)** 및 **교육학적 관점**에서, 각 사회 구성원들의 성향 분포를 이해하는 것은 
국가별 학습 양식(Learning Styles)의 차이나 소통 문화의 다양성을 연구하는 데 중요한 학술적 기초를 제공합니다.
""")

# 데이터 로드 함수 (캐싱을 통해 속도 최적화)
@st.cache_data
def load_data():
    return pd.read_csv("countries_mbti.csv")

try:
    df = load_data()
    
    st.subheader("📊 데이터셋 개요 (Overview)")
    st.write(f"현재 데이터셋에는 총 **{len(df)}개 국가**의 MBTI 비율 정보가 수집되어 있습니다.")
    
    # 데이터프레임 시각화
    st.dataframe(df, use_container_width=True)
    
    # 사이드바 안내
    st.sidebar.success("💡 좌측 메뉴를 선택하여 상세 분석을 진행해 보세요!")
    
    # 학술적 활용 가이드
    st.info("""
    **🧭 대시보드 활용 가이드**
    1. **국가별 MBTI 현황**: 특정 국가를 선택하여 해당 문화권 내에서 어떤 성격 유형이 주류를 이루는지 깊이 있게 탐색합니다.
    2. **MBTI 유형별 국가 비교**: 특정 성격 유형에 집중하여, 어떤 국가나 환경에서 해당 성향이 두드러지게 나타나는지 교차 비교합니다.
    """)
    
except FileNotFoundError:
    st.error("❌ 'countries_mbti.csv' 파일을 찾을 수 없습니다. 파일이 동일한 경로에 있는지 확인해 주세요.")
