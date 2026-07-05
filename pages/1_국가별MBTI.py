import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 MBTI 현황", layout="wide")

st.title("📍 국가별 MBTI 분포 현황")
st.markdown("특정 국가를 선택하여 해당 국가 구성원들의 성격 유형 분포 패턴을 확인하고 학술적 시사점을 도출할 수 있습니다.")

# MBTI 유형별 고유 색상 맵 정의 (시각적 다양성과 아름다움을 위해 파스텔/세련된 톤 배치)
MBTI_COLORS = {
    "INTJ": "#1f77b4", "INTP": "#aec7e8", "ENTJ": "#ff7f0e", "ENTP": "#ffbb78",
    "INFJ": "#2ca02c", "INFP": "#98df8a", "ENFJ": "#d62728", "ENFP": "#ff9896",
    "ISTJ": "#9467bd", "ISFJ": "#c5b0d5", "ESTJ": "#8c564b", "ESFJ": "#c49c94",
    "ISTP": "#e377c2", "ISFP": "#f7b6d2", "ESTP": "#7f7f7f", "ESFP": "#c7c7c7"
}

@st.cache_data
def load_data():
    return pd.read_csv("countries_mbti.csv")

try:
    df = load_data()
    
    # 국가 선택
    countries = sorted(df["Country"].unique())
    selected_country = st.selectbox("📊 분석할 국가를 선택하세요:", countries)
    
    # 데이터 필터링 및 변환
    country_row = df[df["Country"] == selected_country].drop(columns=["Country"]).iloc[0]
    
    # 데이터프레임 구성 및 비율 기준 내림차순(Descending) 정렬
    country_df = pd.DataFrame({
        "MBTI 유형": country_row.index,
        "비율 (Ratio)": country_row.values
    }).sort_values(by="비율 (Ratio)", ascending=False) # 💡 내림차순 정렬 적용
    
    st.subheader(f"📈 [{selected_country}] 성격 유형 분포 우세 순위")
    
    # Plotly를 활용하여 화려하고 세련된 다색(Multi-color) 바 차트 생성
    fig = px.bar(
        country_df, 
        x="MBTI 유형", 
        y="비율 (Ratio)",
        color="MBTI 유형", # 💡 유형별로 색상 다르게 지정
        color_discrete_map=MBTI_COLORS, # 정의한 고유 색상 적용
        text_auto=".2%" # 막대 위에 수치 표시 (가독성 향상)
    )
    
    # 레이아웃 예쁘게 다듬기
    fig.update_layout(
        showlegend=False, # 하단/측면 범례 숨기기 (막대 색상 자체로 구분되므로)
        plot_bgcolor="rgba(0,0,0,0)", # 배경 투명하게
        margin=dict(l=20, r=20, t=20, b=20)
    )
    fig.update_traces(textposition="outside") # 수치를 막대 바깥쪽 위에 표시
    
    # 스트림릿에 차트 그리기
    st.plotly_chart(fig, use_container_width=True)
    
    # 상세 데이터 표 제공
    with st.expander("📄 상세 데이터 보기"):
        st.dataframe(country_df.reset_index(drop=True), use_container_width=True)
        
except FileNotFoundError:
    st.error("❌ 데이터를 불러올 수 없습니다. 'countries_mbti.csv' 파일을 확인해 주세요.")
