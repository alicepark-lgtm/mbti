import streamlit as st
import pandas as pd

st.set_page_config(page_title="국가별 MBTI 현황", layout="wide")

st.title("📍 국가별 MBTI 분포 현황")
st.markdown("특정 국가를 선택하여 해당 국가 구성원들의 성격 유형 분포 패턴을 확인하고 학술적 시사점을 도출할 수 있습니다.")

@st.cache_data
def load_data():
    return pd.read_csv("countries_mbti.csv")

try:
    df = load_data()
    
    # 국가 선택 셀렉트박스
    countries = sorted(df["Country"].unique())
    selected_country = st.selectbox("📊 분석할 국가를 선택하세요:", countries)
    
    # 해당 국가의 데이터만 필터링 후 MBTI 열만 추출
    country_row = df[df["Country"] == selected_country].drop(columns=["Country"]).iloc[0]
    
    # 정보 시각화를 위해 데이터프레임 재구성 및 비율 기준 내림차순 정렬
    country_df = pd.DataFrame({
        "MBTI 유형": country_row.index,
        "비율 (Ratio)": country_row.values
    }).sort_values(by="비율 (Ratio)", ascending=False)  # 가이드라인에 따른 정렬 적용
    
    # 시각화 제시
    st.subheader(f"📈 [{selected_country}] 성격 유형 분포 우세 순위")
    st.bar_chart(data=country_df, x="MBTI 유형", y="비율 (Ratio)", use_container_width=True)
    
    # 상세 데이터 표 제공
    with st.expander("📄 상세 데이터 보기"):
        st.dataframe(country_df.reset_index(drop=True), use_container_width=True)
        
except FileNotFoundError:
    st.error("❌ 데이터를 불러올 수 없습니다. 'countries_mbti.csv' 파일을 확인해 주세요.")
