import bs4
from bs4 import BeautifulSoup
import pandas as pd

# import numpy as np
# import time
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# import re

import os
from os import path
import requests
from urllib.request import urlretrieve

import pymysql 



### 함수 : goods_data(url, mall_category) 
### 입력 : url, cat
### 출력데이터1 : 상품목록 이미지 -> 폴더에 상품목록 이미지 저장
### 출력데이터2 : 메타 데이터(고유id, 이름, 브랜드, 가격, 카테고리, 링크, 리뷰키워드(null)) db에 저장


# 무신사 사이트 상품데이터 크롤링
class GoodsCrawling:
    def __init__(self):
        pass

    def goods_data(self, url, mall_category):

        self.url = url
        self.mall_category = mall_category

        # category_folder 폴더가 없을경우 폴더 생성
        category_code = url.split("/")[-1] 
        path_folder = f"./static/images/musinsa/{mall_category}/{category_code}" 
        if not os.path.isdir(path_folder):
            os.mkdir(path_folder)

        # page를 넘기기 위해서 url 변경
        url = url+"?d_cat_cd=001006&brand=&list_kind=small&sort=pop_category&sub_sort=&page=1&display_cnt=90&group_sale=&exclusive_yn=&sale_goods=&timesale_yn=&ex_soldout=&plusDeliveryYn=&kids=&color=&price1=&price2=&shoeSizeOption=&tags=&campaign_id=&includeKeywords=&measure="

        # 페이지 범위 지정
        start_page = 1
        end_page = 10
        
        # 필요한 리스트를 목록화
        img_link = []    # 썸네일 이미지
        href_list = []   # 상품 링크
        brand_list = []  # 상품 브랜드
        name_list = []   # 상품 이름
        price_list = []    # 상품 가격

        # 페이지 수만큼 반복
        for page in range(start_page, end_page + 1):
            url_sp = url.split("&page=")
            url = f'{url_sp[0]}&page={page}{url_sp[1][1:]}'
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
                "referer": f"https://www.musinsa.com/"
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 필요한 데이터만 선택
                brand_soup = soup.select("div.li_inner > div.article_info > p.item_title > a")
                name_soup = soup.select("div.li_inner > div.article_info > p.list_info > a")
                price_soup = soup.select("div.li_inner > div.article_info > p.price")
                img_soup = soup.select("div.li_inner > div.list_img > a > img")

                # brand_list에 브랜드명을 1개씩 추가
                for brand in brand_soup:
                    brand_list.append(brand.get_text())

                # name_list에 상품명을 1개씩 추가
                for name in name_soup:
                    name_text = name.get_text().strip()
                    if '배송' in name_text:
                        # 필요없는 텍스트 삭제 (EX : 7/12 배송)
                        name_text = name_text.replace(name_text[:20], '').strip()
                    name_list.append(name_text)

                # price_list에 가격을 1개씩 추가
                for price in price_soup:
                    price = price.get_text().strip().split(' ')[-1]
                    price_list.append(price)

                # 썸네일 이미지 URL 저장하기
                for img in img_soup:
                    img_link.append(img.attrs['data-original'])

                # 각 상품의 링크 주소
                for href in name_soup:
                    link = "https:" + href['href']
                    # href_list에 href 주소 추가
                    href_list.append(link)

                # 이미지 파일 다운로드
                for y in range(len(href_list)):
                    product_number = href_list[y].split("/")[-1]
                    urlretrieve(img_link[y], os.path.join(path_folder, f'{product_number}.jpg'))

                print(f"페이지 {page} 이미지 다운로드 완료")
            else:
                print(f"페이지 {page} 불러오기 안됨")

        # 모든 list의 개수가 같으면 실행
        if len(brand_list) == len(name_list) == len(href_list) == len(price_list):
            df = pd.DataFrame(zip(brand_list, name_list, href_list, price_list), columns = ['mall_brand', 'mall_name', 'mall_url', 'mall_price'])
            df['mall_image_id'] = df['mall_url'].str.extract(r'/goods/(\d+)')
            
            df['mall_category'] = mall_category
            df['review_keyword'] = None     

            new_order = ['mall_image_id', 'mall_name', 'mall_brand', 'mall_price', 'mall_category', 'mall_url', 'review_keyword']
            df = df[new_order]


        
            # db 연결
            conn = pymysql.connect(
                    user="root",
                    password="0000",
                    host="localhost",
                    port=3306,
                    database="style_similar",
                    charset='utf8',

                )

            # DataFrame을 리스트로 변환
            data_to_insert = df.values.tolist()

            # db에 저장
            with conn.cursor() as cursor:
                for data in data_to_insert:
                    sql = "INSERT IGNORE INTO board_mall (mall_image_id, mall_name, mall_brand, mall_price, mall_category, mall_url, review_keyword) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, data)
                    conn.commit()

            conn.close()   # 연결 닫기
                
        else :
            print(f"브랜드명 개수:{len(brand_list)} / 상품명:{len(name_list)} / 링크:{len(href_list)} / 상품가격:{len(price_list)}, df 생성에 실패함")

    def main(self):
        # 무신사 카테고리 목록 url, 카테고리 폴더명 입력 (카테고리 폴더는 미리 생성되어있어야 함)
        url = "https://www.musinsa.com/categories/item/001002"
        mall_category = "shirts_blouse"

        # 쇼핑몰상품 카테고리 목록
        # - 셔츠/블라우스 : shirts_blouse
        

        
        # 클래스의 메서드로 변경한 goods_data 메서드를 호출
        self.goods_data(url, mall_category)

if __name__ == "__main__":
    crawling = GoodsCrawling()  # 클래스의 인스턴스 생성
    crawling.main()