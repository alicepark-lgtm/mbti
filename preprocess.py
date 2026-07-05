import pandas as pd

def preprocess_mbti(input_filename, output_filename):
    try:
        # 1. 데이터 불러오기
        df = pd.read_csv(input_filename)
        print(" 데이터가 성공적으로 로드되었습니다.")
        
        # 'Country' 열과 MBTI 데이터 분리
        country_col = df['Country']
        mbti_cols = df.drop(columns=['Country'])
        
        # 2. 열 이름에서 앞 4자리(MBTI 유형)만 추출하여 일괄 변경 (예: INTJ-A -> INTJ)
        mbti_cols.columns = [col[:4] for col in mbti_cols.columns]
        
        # 3. 동일한 MBTI 유형끼리 열을 합산
        # 열(Column) 방향으로 그룹화하여 합산하기 위해 전치(T) 후 groupby를 수행합니다.
        merged_mbti = mbti_cols.T.groupby(level=0).sum().T
        
        # 4. 국가 열과 합산된 MBTI 열을 다시 결합하고, 알파벳 순으로 열을 정렬합니다.
        result_df = pd.concat([country_col, merged_mbti], axis=1)
        mbti_order = sorted(list(merged_mbti.columns))
        result_df = result_df[['Country'] + mbti_order]
        
        # 5. 지정된 파일명으로 결과 저장
        result_df.to_csv(output_filename, index=False)
        print(f" 전처리가 성공적으로 완료되었습니다! 생성된 파일: {output_filename}")
        
    except Exception as e:
        print(f"❌ 전처리 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    # 데이터 구조에 맞게 함수를 호출합니다.
    preprocess_mbti('countries.csv', 'countries_mbti.csv')
