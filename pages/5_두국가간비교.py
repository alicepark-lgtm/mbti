import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="두 국가 간 비교", layout="wide")

st.title("📊 두 국가의 MBTI 비교 분석")
st.markdown("서로 다른 두 국가를 선택하여 16가지 성격 유형 분포가 양적, 질적으로 어떤 차이를 보이는지 대조합니다.")

@st.cache_data
def load_data():
    return pd.read_csv("countries_mbti.csv")

try:
    df = load_data()
    countries = sorted(df["Country"].unique())
    
    col1, col2 = st.columns(2)
    with col1:
        country_a = st.selectbox("🏳️ 첫 번째 국가를 선택하세요:", countries, index=countries.index("South Korea") if "South Korea" in countries else 0)
    with col2:
        # 두 번째 국가는 임의로 다른 국가 지정 가능
        country_b = st.selectbox("🏴 두 번째 국가를 선택하세요:", countries, index=min(1, len(countries)-1))
        
    if country_a == country_b:
        st.warning("⚠️ 서로 다른 두 국가를 선택하셔야 명확한 비교 분석이 가능합니다.")
    else:
        # 두 국가 데이터 추출 및 롱 포맷(Long format)으로 변경
        row_a = df[df["Country"] == country_a].melt(id_vars=["Country"], var_name="MBTI 유형", value_name="비율")
        row_b = df[df["Country"] == country_b].melt(id_vars=["Country"], var_name="MBTI 유형", value_name="비율")
        
        compare_df = pd.concat([row_a, row_b]).sort_values(by="MBTI 유형")
        
        st.subheader(f"⚔️ [{country_a}] vs [{country_b}] 성향 분포 대조 차트")
        
        # 그룹 바 차트(Grouped Bar Chart) 적용
        fig = px.bar(
            compare_df,
            x="MBTI 유형",
            y="비율",
            color="Country",
            barmode="group", # 💡 막대를 나란히 배열하여 직접 비교 가능하게 함
            text_auto=".1f%",
            color_discrete_sequence=["#2ecc71", "#e74c3c"]
        )
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        fig.update_traces(textposition="outside")
        
        st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("❌ 'countries_mbti.csv' 파일을 확인해 주세요.")
