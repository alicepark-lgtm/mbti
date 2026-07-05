import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="우리나라와 비슷한 국가", layout="wide")

st.title("🇰🇷 우리나라와 비슷한 MBTI 분포 국가 탐색")
st.markdown("""
**통계적 유사도 분석(Similarity Analysis)**을 기반으로, 대한민국 구성원들의 MBTI 분포와 가장 높은 상관관계(낮은 오차)를 보이는 문화권을 탐색합니다. 
이를 통해 우리 사회와 심리적·문화적 지형이 유사한 국가들을 학술적으로 유추해볼 수 있습니다.
""")

@st.cache_data
def load_data():
    return pd.read_csv("countries_mbti.csv")

try:
    df = load_data()
    mbti_cols = [col for col in df.columns if col != "Country"]
    
    if "South Korea" not in df["Country"].values:
        # 데이터셋에 'Korea'나 다른 이름으로 되어 있을 수 있으므로 체크 후 안내
        st.warning("⚠️ 데이터셋에서 'South Korea'라는 정확한 이름의 국가를 찾을 수 없습니다. 국가 목록에서 대한민국을 직접 선택해 주세요.")
        target_country = st.selectbox("기준 국가 선택:", sorted(df["Country"].unique()))
    else:
        target_country = "South Korea"
        
    # 기준 국가의 MBTI 벡터 추출
    target_vector = df[df["Country"] == target_country][mbti_cols].iloc[0].values
    
    # 모든 국가와의 평균제곱오차(MSE) 계산 (값이 작을수록 유사함)
    distances = []
    for idx, row in df.iterrows():
        if row["Country"] == target_country:
            continue
        current_vector = row[mbti_cols].values
        # 통계적 거리 계산 (Mean Squared Error)
        mse = np.mean((target_vector - current_vector) ** 2)
        distances.append({"Country": row["Country"], "오차 거리": mse})
        
    distance_df = pd.DataFrame(distances).sort_values(by="오차 거리", ascending=True)
    
    # 유사도 점수로 변환 (오차가 0에 가까울수록 점수는 100점에 가깝게 정규화)
    max_dist = distance_df["오차 거리"].max()
    distance_df["유사도 점수 (%)"] = (1 - (distance_df["오차 거리"] / max_dist)) * 100
    
    st.subheader(f"🏆 [{target_country}]와 MBTI 성향이 가장 닮은 글로벌 Top 10 국가")
    top_10 = distance_df.head(10).sort_values(by="유사도 점수 (%)", ascending=False)
    
    fig = px.bar(
        top_10,
        x="유사도 점수 (%)",
        y="Country",
        orientation="h",  # 가독성을 위한 수평 바 차트
        text_auto=".1f",
        color="유사도 점수 (%)",
        color_continuous_scale="Plotly3"
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False)
    fig.update_traces(textposition="outside")
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 교육학적 해석 피드백 비계 설정
    st.info(f"💡 **해석 가이드**: 유사도 점수가 100%에 가까울수록 {target_country}의 성격 유형 분포 비율과 거의 일치함을 의미합니다. 이 국가들과의 교육 시스템, 기업 문화, 사회적 소통 방식을 비교 연구하면 흥미로운 비교교육학적 인사이트를 얻을 수 있습니다.")

except FileNotFoundError:
    st.error("❌ 'countries_mbti.csv' 파일을 확인해 주세요.")
