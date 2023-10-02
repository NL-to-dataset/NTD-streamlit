#import pickle
import re
#import sys
import bareunpy as brn

import pandas as pd
#대체 단어 사진 불러옴
filepath_synonym='C:\\Users\\ykhwang\\Desktop\\streamlit-app\\syn_dict.txt'
#불용어 사진 불러옴
filepath_stop='C:\\Users\\ykhwang\\Desktop\\streamlit-app\\stop_dict.txt'

API_KEY="koba-Y33XMJI-OWGE5UY-RQFR3MA-4I6UN2Q"

class Preprocess_text:
	# 생성자
  def __init__(self):

		# 형태소 분석기 초기화
    self.brn =  brn.Tagger(API_KEY, 'localhost', port=5656)

	# 형태소 분석기 POS tagger (래퍼 함수)
  def pos(self, sentence):
    #대체어 사전 구축
    replacement_dict = {}
    with open(filepath_synonym, 'r', encoding='utf-8') as file:
      for line in file:
        original, replacement = line.strip().split('\t')
        replacement_dict[original] = replacement
    for original, replacement in replacement_dict.items():
      sentence = sentence.replace(original,replacement)

      #불용어 사전 구축
    stop_word_list = []
    with open(filepath_stop, 'r', encoding='utf-8') as file:
      for line in file:
        stop_word_list.append(line.strip())

      #print(stop_word_list)

      for stop_word in stop_word_list:

        sentence = sentence.replace(stop_word,'')



    #형태소 분석 결과 반환
    return self.brn.pos(sentence)



#기간 키워드 추출 메소드 작성
def get_duration_keywords(self, morphemes):
     duration_keywords=[]
     current_word = ""
     keyword_pattern = r'(\d+년|\d+개월|최근)'
     #6개월->6+개월로 어절이 나누어져 분석되는걸, 하나의 어절 기간 키워드로 받아옴
     for morpheme, pos in morphemes:

      duration_keyword = re.findall(keyword_pattern, morpheme)
      if duration_keyword:
                #duration_keywords.append(duration_keyword[0])
                duration_keywords=duration_keyword[0]

      if pos == 'SN' or pos == 'NNB':
        current_word += morpheme
      else:
        if current_word:
            duration_keywords.append(current_word)
            current_word = ""


     print("기간 키워드:", duration_keywords)
     return duration_keywords


#주제 키워드 추출 메소드 작성
#불용어 사전 추가하지 않음
def get_title_keywords(self,pos_tag,duration_keywords=''):
    nnp_keywords=[]
    #stop_keywords=[]
    duration_keywords=duration_keywords
    for word_tag in pos_tag:
        if word_tag[1] == 'NNP' or word_tag[1] == 'NNG':
            nnp_keywords.append(word_tag[0])
    #고유명사 키워드 리스트에서 기간 키워드 제외
    if duration_keywords in nnp_keywords:
        nnp_keywords.remove(duration_keywords)
    print("추출된 고유명사:", nnp_keywords)

    print("추출된 주제 키워드:", nnp_keywords)
    return nnp_keywords


# Preprocess 클래스에 메서드를 추가
Preprocess_text.get_duration_keywords = get_duration_keywords
Preprocess_text.get_title_keywords =get_title_keywords

#기간 키워드 추출 메소드 작성
def get_duration_keywords(self, pos):
    duration_keywords=[]
    keyword_pattern = r'(\d+년|\d+개월|최근)'

    for word,pos_tag in pos:
            duration_keyword = re.findall(keyword_pattern, word)
            if duration_keyword:
                #duration_keywords.append(duration_keyword[0])
                duration_keywords=duration_keyword[0]


    print("기간 키워드:", duration_keywords)
    return duration_keywords

#전처리코드 테스트

import streamlit as st
st.title('My First Streamlit App')
user_query=st.text_input('질의어를 입력하세요.',help='도서, 영상, 뉴스 등 찾고 싶은 데이터셋에 대해 물어보세요.',placeholder='인기있는 도서 데이터셋 찾아줘')

#text ="인기 있는 도서 데이터셋 찾아줘"
text = user_query
my_tagger = Preprocess_text()
#형태소 분석기 실행
pos=my_tagger.pos(text)
print(pos)
duration_keywords = my_tagger.get_duration_keywords(pos)
title_keywords = my_tagger.get_title_keywords(pos,duration_keywords=duration_keywords)

#추출한 키워드 df생성
for keyword in title_keywords:
    title_keywords_all=' '.join(title_keywords)

df = pd.DataFrame({'period': [duration_keywords], \
        'title': title_keywords_all})
print(df)

#형태소 태그 제외
noposlist=[]
for pos_tuple in pos:

  noposlist.append(pos_tuple[0])


text_nopos = ' '.join(noposlist)
print(text_nopos)

from keybert import KeyBERT
kw_model = KeyBERT()

keywords = kw_model.extract_keywords(text_nopos,keyphrase_ngram_range=(1,1),stop_words=None, top_n=20)
print(keywords)

#중요도 랭킹 제외
keywordlist=[]
for key_tuple in keywords:

  keywordlist.append(key_tuple[0])


#text_noranking = ' '.join(keywordlist)
print(keywordlist)


filepath_title='C:\\Users\\ykhwang\\Desktop\\streamlit-app\\title_dict.txt'
title=[]
with open(filepath_title, 'r', encoding='utf-8') as file:
  for line in file:
    title.append(line.strip())
#print(title)


filepath_domain='C:\\Users\\ykhwang\\Desktop\\streamlit-app\\domain_dict.txt'
domain=[]
with open(filepath_domain, 'r', encoding='utf-8') as file:
  for line in file:
    domain.append(line.strip())

filepath_period='C:\\Users\\ykhwang\\Desktop\\streamlit-app\\period-dict.txt'
period=[]
with open(filepath_period, 'r', encoding='utf-8') as file:
  for line in file:
    period.append(line.strip())
domain_word=""
title_word=""
period_word=""
specific_word=""
book_csv_file_path = "C:\\Users\\ykhwang\\Desktop\\streamlit-app\\교보문고 it 주간 베스트셀러 크롤링100.csv"
video_csv_file_path = "C:\\Users\\ykhwang\\Desktop\\streamlit-app\\youtube_2달블랙핑크.csv"
for keyword in keywordlist:
  if keyword in title:
    title_word=keyword
    
  elif keyword in domain:
    domain_word=keyword
      
  elif keyword in period:
    period_word=keyword
  else:
    specific_word=keyword

df=pd.DataFrame({'title':[title_word],
                             'domain':[domain_word],
                             'period':[period_word],
              'specific':[specific_word]
              })
print(df)
print(domain_word)

if domain_word=="도서":
  st.text('주간 종합 베스트셀러에 대한 데이터셋을 제공합니다.')
  df = pd.read_csv(book_csv_file_path)
  st.dataframe(df)
elif domain_word=="영상":
  st.text('블랙핑크 유튜브 영상에 대한 데이터셋을 제공합니다.')
  df = pd.read_csv(video_csv_file_path)
  st.dataframe(df)

@st.cache
def convert_df(df):
# IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8-sig')

csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)