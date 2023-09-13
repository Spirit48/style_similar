# pip install requests
# pip install chardet
# pip install lxml
# pip install selenium
# pip install webdriver-manager
# pip install keras
# pip install scikit-learn
# pip install kiwipiepy

import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd

import os
from urllib.request import urlretrieve
import selenium
import re

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.action_chains import ActionChains

import time

import numpy as np

from sklearn.model_selection import train_test_split
from kiwipiepy import Kiwi


from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


from tensorflow.keras.layers import Embedding, Dense, GRU
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

import pymysql



stopwords = ['도', '는', '다', '의', '가', '이', '은', '한', '에', '하', '고', '을', '를', '인', '듯', '과', '와', '네', '들', '듯', '지', '임', '게']
kiwi = Kiwi()

def tokenizing(sentence):
    # 불용어 제거 : 긍정을 평가하는데 필요없는 접속사 등을 제거하기 위함

    try:
        if not sentence:
            raise ValueError
            
        # kiwi tokenize를 이용하여 문장을 token화 하고 stopwords에 포함되는 단어가 있으면 포함 x
        words = [token[0] for token in kiwi.tokenize(sentence) if token[0] not in stopwords]
    
    except ValueError as e:
        print(e)
    
    return words


# 학습모델에 필요한 사전학습데이터 생성
def train_data():
    # 사전학습 데이터 naver_shopping.txt 
    df = pd.read_csv("naver_shopping.txt", sep="\t", header=None, encoding="utf-8-sig")
    df.columns = ['score', 'reviews']

    # df.score 값이 3 초과인 값을 1로, 기본값을 0으로 설정해서 laebl column을 추가해 저장
    df['label'] = np.select([df.score > 3], [1], default=0) 

    # Drop_duplicate : 중복 삭제
    df.drop_duplicates(subset=['reviews'], inplace=True) # subset : columns에서 결측치 있는 행 삭제

    df['reviews'] = df['reviews'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣]", "", regex=True) # 한글을 제외한 나머지 문자열을 선택, 공백으로 없애줌
    df['reviews'].replace('', np.nan, inplace=True) # 빈 공백은 nan 결측치로 변경함

    train_data, test_data = train_test_split(df, # 데이터셋
                                            test_size=0.2, # train : test를 4:1로 분리 
                                            random_state=0) # 랜덤 규칙을 0으로 설정

    # train, test 데이터에 tokenizing 함수 적용 -> 문장을 단어로 나눠줌
    print("토크나이징 시작")  
    train_data['tokenized']=train_data['reviews'].apply(tokenizing) 
    test_data['tokenized']=test_data['reviews'].apply(tokenizing)

    # negative_words = np.hstack(train_data[train_data.label == 0]['tokenized'].values)  # positive 값만 선택해 numpy로 합침(horizontal stack)
    # positive_words = np.hstack(train_data[train_data.label == 1]['tokenized'].values)  # negative 값만 선택해 numpy로 합침(horizontal stack)
    # negative_word_count = Counter(negative_words) # Counter : 각 변수값의 빈도수를 알려줌
    # print(negative_word_count.most_common(20)) # most_common(n) : 가장 많은 값을 n개 보여줌
    # positive_word_count = Counter(positive_words)
    # print(positive_word_count.most_common(20))

    X_train = train_data['tokenized'].values # 토큰화된 
    y_train = train_data['label'].values     # 긍정/부정 정답
    X_test = test_data['tokenized'].values
    y_test = test_data['label'].values       # 긍정/부정 정답

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X_train) # X_train data를 tokenizer 시킴 -> X_train의 단어들을 받아 토큰화(단어별 정수인코딩)
    rare_max=2

    total_cnt = len(tokenizer.word_index) # 정수인코딩 단어 개수
    rare_cnt = 0   # 단어가 1개밖에 없는 개수를 카운트
    total_freq = 0 # 
    rare_freq = 0

    for _, value in tokenizer.word_counts.items():  # dictionary로 이루어진 {단어 : 정수값} 형태를 하나씩 불러옴
        total_freq = total_freq + value               # 단어의 중복 개수를 저장

        # 중복된 단어의 개수가 1개인 값의 개수를 저장
        if value < rare_max:  
            rare_cnt += 1        
            rare_freq = rare_freq + value

    vocab_size = total_cnt - rare_cnt + 2 # 2는 시작토큰, 종료 토큰을 의미

    # 정수 인코딩 과정에서 vocab_size 보다 큰 숫자가 부여된 단어들은 OOV로 변환
    tokenizer = Tokenizer(vocab_size, oov_token='OOV') # OOV : Out Of Vocabulary
    tokenizer.fit_on_texts(X_train) 
    X_train = tokenizer.texts_to_sequences(X_train) # 정수시퀀스로 변환
    X_test = tokenizer.texts_to_sequences(X_test)

    # 패딩 설정
    max_len = 75
    X_train = pad_sequences(X_train, maxlen=max_len)
    X_test = pad_sequences(X_test, maxlen=max_len)

    return X_train, y_train, X_test, y_test, vocab_size, tokenizer, max_len

# GRU 모델
def model_gru(X_train, y_train, vocab_size):


    embedding_dim = 100
    hidden_units = 256 

    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim))
    model.add(GRU(hidden_units))
    model.add(Dense(1, activation='sigmoid'))

    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=4)
    mc = ModelCheckpoint('gru_256.h5', monitor='val_loss', mode='min', verbose=1, save_best_only=True)

    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])
    history = model.fit(X_train, y_train, epochs=20, callbacks=[es, mc], batch_size=64, validation_split=0.2)


# 사전학습모델 생성
X_train, y_train, X_test, y_test, vocab_size, tokenizer, max_len = train_data()

# 모델 학습
# model_gru(X_train, y_train, vocab_size)  

# 모델 평가
loaded_model = load_model('gru_256.h5')  #저장한 모델을 불러옴
print('GRU 모델 정확도 : %.4f' % (loaded_model.evaluate(X_test, y_test)[1]))



# review_make() : 상품의 모든 댓글 데이터를 가져옴
def review_make(url, driver):
    # 댓글 가져올 무신사 상품상세페이지 이동
    driver.get(url) 

    # 신규회원 레이어팝업이 뜰때까지 기다렸다가 새로고침
    time.sleep(10) 
    driver.refresh() 
    
    # html 긁어오기
    html = driver.page_source
    soup = BeautifulSoup(html,"lxml")

    review_list = []
    grade_list = []

    # 첫번째 페이지 댓글 저장
    review_soup = soup.select("#reviewListFragment  div.review-contents > div.review-contents__text")
    for review in review_soup:
        review_list.append(review.get_text().strip())

    # 첫번째 페이지 평점 저장
    # grade_soup = soup.select("#reviewListFragment  div.review-list__rating-wrap > span > span > span")
    # for grade in grade_soup:
    #     grade_num= re.sub(r'[^0-9]', '', str(grade)) 
    #     # 평점이 4, 5점이면 positive(1), 3점 이하면 negative(0) 
    #     grade_list.append(1 if int(grade_num) >= 80 else 0) 


    # 댓글저장 최대 반복횟수 계산
    review_num = soup.select("#reviewListFragment > div.nslist_bottom > div.box_page_msg") 
    review_num_max = int(review_num[0].get_text().strip().split()[0])

    btn_num = 0
    # 각 block의 첫번째 댓글목록을 불러와서 댓글 저장
    for i in range(review_num_max-1):

        # 다음버튼 클릭
        driver.find_element(By.XPATH, f'//*[@id="reviewListFragment"]/div[11]/div[2]/div/a[{btn_num+4}]').send_keys(Keys.ENTER)


        # 2번버튼 : 4, 3번버튼 : 5, 4번버튼 : 6, 5번버튼 : 7, 다음버튼 : 8
        time.sleep(1)
        btn_num += 1
        if btn_num == 5:
            btn_num = 0

        # 나머지 페이지 댓글 저장
        html = driver.page_source
        soup = BeautifulSoup(html,"lxml")
        review_soup = soup.select("#reviewListFragment  div.review-contents > div.review-contents__text")
        for review in review_soup:
            review_list.append(review.get_text().strip())

        # 나머지 페이지 평점 저장
        # grade_soup = soup.select("#reviewListFragment  div.review-list__rating-wrap > span > span > span")
        # for grade in grade_soup:
        #     grade_num= re.sub(r'[^0-9]', '', str(grade))
        #     grade_list.append(1 if int(grade_num) >= 80 else 0) 
    
    dataset = pd.DataFrame(review_list, columns=['review'])
    return dataset

# 댓글 감정분석 함수
def sentiment_predict(dataset):
    review_sentence = list(dataset.review) # dataset으로 review의 데이터들을 가져옴 -> list로 변환
    sentiment_list = []
    
    for sentence in review_sentence:
        sentence = re.sub('r[^ㄱ-ㅎㅏ-ㅣ가-힣]', '', sentence)
        sentence = tokenizing(sentence)
        encoded = tokenizer.texts_to_sequences([sentence])
        pad_new = pad_sequences(encoded, maxlen = max_len)
        score = float(loaded_model.predict(pad_new))

        if score > 0.9:               # 긍정도가 90% 이상인 값을 긍정으로 설정
            sentiment_list.append(1)
        else:
            sentiment_list.append(0)
            
    dataset["sentiment"] = sentiment_list

    return dataset

# 긍정 댓글 dataset을 입력하면 긍정 keyword를 호출하는 함수
def tokenizing_pos(dataframe):
    word_list = []
    noun_list = []
    keyword = ''
    words = pd.DataFrame()
    
    for sentence in dataframe['review']:
        for token in kiwi.tokenize(sentence):
            if token[1] == 'NNG': 
                word_list.append(token[0])
                noun_list.append(token[1])

    words['word'] = word_list
    word_pos= words['word'].value_counts().index[:20]
    
    break_point = 0
    for word in word_pos:
        if  break_point == 3:
            break
        
        if '핏' in word or '디자인' in word or '코디' in word:
            if '핏이 예뻐요' not in keyword:
                keyword = keyword + '핏이 예뻐요 '
                break_point += 1

        if '가성비' in word or '가격' in word:
            if '가성비가 좋아요' not in keyword:
                keyword = keyword + '가성비가 좋아요 '
                break_point += 1

        if '기장' in word:
            if '기장이 딱 맞아요' not in keyword:
                keyword = keyword + '기장이 딱 맞아요 '
                break_point += 1

        if '두께' in word:
            if '두께감이 적당해요' not in keyword:
                keyword = keyword + '두께감이 적당해요 '
                break_point += 1

        if '재질' in word or '소재' in word or '원단' in word:
            if '좋은 소재를 사용해요' not in keyword:
                keyword = keyword + '좋은 소재를 사용해요 '
                break_point += 1

        if '색' in word or '색상' in word or '색감' in word:
            if '실제 색감이 예뻐요' not in keyword:
                keyword = keyword + '실제 색감이 예뻐요 '
                break_point += 1

        if '운동' in word:
            if '운동할때 입기 좋아요' not in keyword:
                keyword = keyword + '운동할때 입기 좋아요 '
                break_point += 1
            
    return keyword






# mariadb 접속
conn = pymysql.connect(
        user="root",
        password="0000",
        host="localhost",
        port=3306,
        database="style_similar",
        charset='utf8',
    )

cursor = conn.cursor()


# SQL 쿼리 실행 - mall_image_id, mall_url을 가져옴
sql_query = "SELECT mall_image_id, mall_url  FROM board_mall"
cursor.execute(sql_query)

# 결과 가져오기
data = cursor.fetchall()



# 크롬 드라이버 생성
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 결과 출력
count = 0
for row in data:
    mall_image_id = row[0]  # mall_image_id
    url = row[1]            # mall_url 
    review_dataset = review_make(url, driver)
    sentiment_dataset = sentiment_predict(review_dataset)

    # mall_image_id column 추가 -> 각 리뷰들이 어떤 상품의 리뷰인지 표시
    sentiment_dataset['mall_image_id'] = mall_image_id

    # DataFrame을 리스트로 변환
    data_board_review = sentiment_dataset.values.tolist()
    
    print(data_board_review)

    # board_review에 댓글, 댓글감성분석결과, 상품 id를 db에 저장
    with conn.cursor() as cursor:
        for data in data_board_review:
            sql = "INSERT IGNORE INTO board_review (review, review_sentiment, mall_image_id_id) VALUES (%s, %s, %s)"
            cursor.execute(sql, data)
            conn.commit()




    # 댓글이 긍정인 데이터셋을 입력
    sentiment_dataset_pos = sentiment_dataset[sentiment_dataset['sentiment']==1]
    review_keyword = tokenizing_pos(sentiment_dataset_pos)

    sentiment_percent = sentiment_dataset['sentiment'].value_counts(normalize=True)[1]
    sentiment_percent = "{:.2%}".format(sentiment_percent) 
    
    data_board_review = [review_keyword, mall_image_id]

    # board_mall에 상품 id에 keyword들을 업데이트
    with conn.cursor() as cursor:
        sql = "UPDATE board_mall SET review_keyword = %s WHERE mall_image_id = %s"
        cursor.execute(sql, data_board_review)
        conn.commit()
    
    count += 1

    if count == 10:
        break

# 연결 종료
cursor.close()
conn.close()
driver.quit()


print("전체 크롤링, db저장 완료!!!")
