import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MBTI 유형별 국가 비교", layout="wide")

st.title("🔍 MBTI 유형별 글로벌 비교 분석")
st.markdown("특정 MBTI 유형이 어떤 문화권이나 국가에서 상대적으로 더 높은 빈도로 나타나는지 정량적으로 비교합니다.")

@st.cache_data
def load_data():
    return pd.read_csv("countries_mbti.csv")

try:
    df = load_data()
    
    # MBTI 유형 리스트 추출
    mbti_types = [col for col in df.columns if col != "Country"]
    selected_mbti = st.selectbox("✨ 비교 분석할 MBTI 유형을 선택하세요:", mbti_types)
    
    # 정렬 및 필터링
    comparison_df = df[["Country", selected_mbti]].sort_values(by=selected_mbti, ascending=False)
    
    st.subheader(f"🏆 {selected_mbti} 유형 비율이 높은 국가 순위")
    top_n = st.slider("표시할 상위 국가 수를 선택하세요:", min_value=5, max_value=len(comparison_df), value=15)
    
    filtered_df = comparison_df.head(top_n)
    
    # Plotly 바 차트 생성
    fig = px.bar(
        filtered_df,
        x="Country",
        y=selected_mbti,
        # 💡 text_auto='.2%' 설정으로 마우스를 올리지 않아도 소수점 둘째 자리 퍼센트(%)가 막대 위에 항상 노출됩니다.
        text_auto=".2%", 
        color=selected_mbti, # 비율에 따른 그라데이션 색상 적용
        color_continuous_scale="Viridis" # 세련된 색상 스케일
    )
    
    # 디자인 디테일 수정
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, # 색상 바 숨겨서 차트를 더 넓게 쓰기
        margin=dict(l=20, r=20, t=20, b=20)
    )
    fig.update_traces(textposition="outside") # 💡 텍스트가 항상 막대 '위쪽 바깥'에 고정되도록 설정
    
    # 차트 출력
    st.plotly_chart(fig, use_container_width=True)
    
    # 상세 데이터 표 제공
    with st.expander("📄 순위 데이터 표 확인하기"):
        st.dataframe(comparison_df.reset_index(drop=True), use_container_width=True)

except FileNotFoundError:
    st.error("❌ 데이터를 불러올 수 없습니다. 'countries_mbti.csv' 파일을 확인해 주세요.")
