import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="4대 지표별 분석", layout="wide")

st.title("🧭 글로벌 4대 양극 지표(Dichotomies) 분석")
st.markdown("16가지 복합 MBTI 유형을 성격 심리학의 기본 축인 **E/I(외향/내향), N/S(직관/감각), T/F(사고/감정), J/P(판단/인식)**으로 분해하여 국가별 차이를 탐색합니다.")

@st.cache_data
def load_data():
    return pd.read_csv("countries_mbti.csv")

try:
    df = load_data()
    
    # 4대 지표 계산 로직 함수
    def calculate_dichotomies(data):
        calc_df = pd.DataFrame()
        calc_df["Country"] = data["Country"]
        
        # 각 지표에 해당하는 성향들의 합 계산
        calc_df["E"] = data[["ENFJ", "ENFP", "ENTJ", "ENTP", "ESFJ", "ESFP", "ESTJ", "ESTP"]].sum(axis=1)
        calc_df["I"] = data[["INFJ", "INFP", "INTJ", "INTP", "ISFJ", "ISFP", "ISTJ", "ISTP"]].sum(axis=1)
        calc_df["N"] = data[["ENFJ", "ENFP", "ENTJ", "ENTP", "INFJ", "INFP", "INTJ", "INTP"]].sum(axis=1)
        calc_df["S"] = data[["ESFJ", "ESFP", "ESTJ", "ESTP", "ISFJ", "ISFP", "ISTJ", "ISTP"]].sum(axis=1)
        calc_df["T"] = data[["ENTJ", "ENTP", "ESTJ", "ESTP", "INTJ", "INTP", "ISTJ", "ISTP"]].sum(axis=1)
        calc_df["F"] = data[["ENFJ", "ENFP", "ESFJ", "ESFP", "INFJ", "INFP", "ISFJ", "ISFP"]].sum(axis=1)
        calc_df["自由"] = data[["ENFJ", "ENTJ", "ESFJ", "ESTJ", "INFJ", "INTJ", "ISFJ", "ISTJ"]].sum(axis=1) # J 의미
        calc_df["P"] = data[["ENFP", "ENTP", "ESFP", "ESTP", "INFP", "INTP", "ISFP", "ISTP"]].sum(axis=1)
        calc_df.rename(columns={"自由": "J"}, inplace=True)
        return calc_df

    dicho_df = calculate_dichotomies(df)
    
    # 분석하고 싶은 지표 선택
    indicator = st.selectbox("✨ 분석할 성향 축을 선택하세요:", ["E (외향형) vs I (내향형)", "N (직관형) vs S (감각형)", "T (사고형) vs F (감정형)", "J (판단형) vs P (인식형)"])
    
    left_char, right_char = indicator.split(" vs ")[0][0], indicator.split(" vs ")[1][0]
    
    # 시각화를 위해 해당 지표 기준으로 내림차순 정렬
    plot_df = dicho_df[["Country", left_char, right_char]].sort_values(by=left_char, ascending=False)
    
    st.subheader(f"📊 {indicator} 글로벌 분포 현황 (상위 15개국)")
    top_n_df = plot_df.head(15)
    
    # 누적 막대 그래프(Stacked Bar Chart)를 통해 두 성향의 비율 결합 시각화
    fig = px.bar(
        top_n_df, 
        x="Country", 
        y=[left_char, right_char],
        barmode="stack",
        text_auto=".1f%",
        color_discrete_sequence=["#4A90E2", "#F5A623"] # 세련된 대비 색상
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", legend_title_text="성향 지표")
    
    st.plotly_chart(fig, use_container_width=True)

except FileNotFoundError:
    st.error("❌ 'countries_mbti.csv' 파일을 확인해 주세요.")
