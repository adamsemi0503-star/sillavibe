import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Streamlit의 캐싱 기능을 사용하여 데이터 로딩 속도를 향상시킵니다.
@st.cache_data
def load_data(file_path):
    """CSV 파일을 읽어와서 pandas DataFrame으로 변환하는 함수"""
    if not os.path.exists(file_path):
        st.error(f"오류: '{file_path}' 경로에 파일이 없습니다. 파일 경로를 확인해주세요.")
        return None
    try:
        # 한글 파일명과 내용을 올바르게 읽기 위해 'utf-8-sig' 인코딩을 사용합니다.
        data = pd.read_csv(file_path, encoding='utf-8-sig')
        return data
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

def main():
    """메인 애플리케이션 함수"""
    # --- 페이지 설정 ---
    st.set_page_config(page_title="경제활동인구 대시보드", layout="wide")

    st.title("📈 연도별/지역별 경제활동인구 대시보드")
    st.markdown("`경제활동_통합 (1).csv` 파일의 데이터를 시각화합니다.")

    # --- 데이터 로드 ---
    # CSV 파일의 전체 경로를 지정합니다.
    file_path = r'd:\컴퓨터_공학부_202295004_김민석\AI 수업2\경제활동_통합 (1).csv'
    df = load_data(file_path)

    if df is not None:
        # --- 사이드바 필터 ---
        st.sidebar.header("🔎 데이터 필터")
        # '년도' 컬럼에서 고유한 값들을 가져와 내림차순으로 정렬합니다.
        years = sorted(df['년도'].unique(), reverse=True)
        selected_year = st.sidebar.selectbox('년도를 선택하세요', years)

        # --- 데이터 필터링 ---
        filtered_df = df[df['년도'] == selected_year]

        # --- 데이터 시각화 ---
        st.header(f"📊 {selected_year}년 지역별 경제활동인구 (단위: 천명)")

        # '계' 행을 제외하고 시각화를 위해 데이터를 준비합니다.
        chart_data = filtered_df[filtered_df['지역'] != '계']
        # '지역'을 인덱스로 설정하여 차트의 x축 레이블로 사용합니다.
        chart_data = chart_data.set_index('지역')

        # 막대 그래프를 그립니다.
        st.bar_chart(chart_data['경제활동인구 (천명)'])

        # --- 원본 데이터 표시 ---
        st.header(f"📄 {selected_year}년 상세 데이터")
        st.dataframe(filtered_df)

        # 전체 데이터 표시 옵션
        if st.checkbox('전체 원본 데이터 보기'):
            st.header(" 전체 원본 데이터")
            st.dataframe(df)

if __name__ == "__main__":
    main()
