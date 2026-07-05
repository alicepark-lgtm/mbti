import streamlit as st
import pandas as pd

st.set_page_config(page_title="MBTI 유형별 국가 비교", layout="wide")

st.title("🔍 MBTI 유형별 글로벌 비교 분석")
st.markdown("특정 MBTI 유형이 어떤 문화권이나 국가에서 상대적으로 더 높은 빈도로 나타나는지 정량적으로 비교합니다.")

@st.cache_data
def load_data():
    return pd.read_csv("countries_mbti.csv")

try:
    df = load_data()
    
    # MBTI 유형 리스트 추출 (Country 제외)
    mbti_types = [col for col in df.columns if col != "Country"]
    selected_mbti = st.selectbox("✨ 비교 분석할 MBTI 유형을 선택하세요:", mbti_types)
    
    # 해당 MBTI 열과 국가 열만 추출하여 비율 기준 내림차순 정렬
    comparison_df = df[["Country", selected_mbti]].sort_values(by=selected_mbti, ascending=False)
    
    # 국가가 너무 많을 경우 가독성이 떨어지므로, 사용자가 상위 N개 국가를 조절할 수 있도록 슬라이더 제공
    st.subheader(f"🏆 {selected_mbti} 유형 비율이 높은 국가 순위 (정렬 완료)")
    top_n = st.slider("표시할 상위 국가 수를 선택하세요:", min_value=5, max_value=len(comparison_df), value=15)
    
    filtered_df = comparison_df.head(top_n)
    
    # 바 차트 시각화
    st.bar_chart(data=filtered_df, x="Country", y=selected_mbti, use_container_width=True)
    
    # 상세 데이터 표 제공
    with st.expander("📄 순위 데이터 표 확인하기"):
        st.dataframe(comparison_df.reset_index(drop=True), use_container_width=True)

except FileNotFoundError:
    st.error("❌ 데이터를 불러올 수 없습니다. 'countries_mbti.csv' 파일을 확인해 주세요.")
