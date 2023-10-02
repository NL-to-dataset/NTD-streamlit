import streamlit as st
import re
import pandas as pd

st.title('My First Streamlit App')
user_query=st.text_input('질의어를 입력하세요.',help='도서, 영상, 뉴스 등 찾고 싶은 데이터셋에 대해 물어보세요.',placeholder='인기있는 도서 데이터셋 찾아줘')
pattern = r"\b인기\b"
#st.text(user_query)

csv_file_path = "C:\\Users\\ykhwang\\Desktop\\streamlit-app\\교보문고 it 주간 베스트셀러 크롤링100.csv"

if re.search(pattern, user_query):
    print("문장에 '인기' 단어가 포함되어 있습니다.")
    st.text('주간 종합 베스트셀러에 대한 데이터셋을 제공합니다.')
    df = pd.read_csv(csv_file_path)
    st.dataframe(df)

    @st.cache
    def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='large_df.csv',
        mime='text/csv',
    )

