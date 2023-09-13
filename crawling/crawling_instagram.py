from urllib.request import urlopen, urlretrieve
from urllib.parse import quote_plus as qp  

import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pandas as pd
import time
import os
import pymysql

# from bs4 import BeautifulSoup
# import requests
# import cv2



class InstaCrawling:
    # 인스타그램 로그인 함수 정의
    def login(self, id, pw, driver):
        
        self.id = id
        self.pw = pw
        self.driver = driver
    
        # 로그인 페이지로 이동
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(1)

        # 텍스트 입력 요소(id, pw) 모두 찾기
        input = driver.find_elements(By.TAG_NAME, "input")

        # id 입력
        input[0].send_keys(id)

        # pw 입력
        input[1].send_keys(pw)

        # 엔터 버튼 클릭
        input[1].send_keys(Keys.RETURN)
        time.sleep(5)

        # # 로그인 정보 저장 여부 팝업창 제거 ("나중에 하기 버튼 클릭")
        # driver.find_element(By.CLASS_NAME, '_ac8f').click()
        # time.sleep(3)

        # # 알림 설정 팝업창 제거 ("나중에 하기 버튼 클릭")
        # driver.find_element(By.CLASS_NAME, '_a9--._a9_1').click()


    def insta_url(self, url, path_folder, driver):

        self.url = url
        self.path_folder = path_folder
        self.driver = driver

        insta_url_list = []
        
        # 폴더가 없으면 폴더 생성
        if not os.path.isdir(path_folder):
            os.mkdir(path_folder)

        driver.get(url) # 해당 페이지 이동
        time.sleep(3)

        # 스크롤 횟수 입력 - 수가 높을수록 해당 계정의 많은 게시물의 데이터를 저장
        for _ in range(10):
            # 현재 스크롤 높이
            scroll_location = driver.execute_script("return document.body.scrollHeight")

            # 스크롤 맨 밑으로 내림
            scroll_script = "window.scrollTo(0, document.body.scrollHeight);"
            driver.execute_script(scroll_script)

            #전체 스크롤이 늘어날 때까지 대기
            time.sleep(2)
            
            #늘어난 스크롤 높이
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            
            #늘어난 스크롤 위치와 이동 전 위치 같으면(더 이상 스크롤이 늘어나지 않으면) 종료
            if scroll_location == scroll_height:
                break

            #같지 않으면 스크롤 위치 값을 수정하여 같아질 때까지 반복
            else:
                #스크롤 위치값을 수정
                scroll_location = driver.execute_script("return document.body.scrollHeight")

            links = driver.find_elements(By.CSS_SELECTOR, "article > div:nth-child(1) > div  a")
            for link in links:
                insta_url = link.get_attribute("href")

                if insta_url not in insta_url_list:
                    insta_url_list.append(insta_url)
        
        return insta_url_list
    

    def naver_shopping(self, insta_product_name, driver):
        self.driver = driver

        if '&' in insta_product_name:
            insta_product_name = insta_product_name.replace('&', '%26')

        if ',' in insta_product_name:
            insta_product_name = insta_product_name.split(',')[0]

        naver_shop = f'https://search.shopping.naver.com/search/all?query={insta_product_name}'
        driver.get(naver_shop)
        driver.implicitly_wait(10)

        # 네이버쇼핑 카테고리 내용 (패션의류 > 여성의류 > 재킷)
        category_list = driver.find_elements(By.XPATH, "//* /div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/span")
        category = ''

        if category_list:
            category = category_list[-1].text

        # 검색 결과가 없을 때 재검색
        else:
            # 맨 첫번째 단어만 검색
            insta_product_name = insta_product_name.split()[0]
            naver_shop = f'https://search.shopping.naver.com/search/all?query={insta_product_name}'
            driver.get(naver_shop)
            driver.implicitly_wait(10)

            category_list = driver.find_elements(By.XPATH, "//* /div[1]/div[2]/div/div[1]/div/div/div[2]/div[3]/span")
            if category_list:
                category = category_list[-1].text



        return category




    def insta_data(self, insta_url, path_folder, driver):

        self.insta_url = insta_url
        self.path_folder = path_folder
        self.driver = driver
        
        driver.get(insta_url) # 해당 페이지 이동
        driver.implicitly_wait(10)

        try:
            # 인스타 이미지와 게시물의 내용을 가져옴
            image = driver.find_elements(By.XPATH, "//* /section/main/div/div[1]/div/div[1]/div/div/div/div/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div[1]/div[1]/img")    
            if image == []:
                image = driver.find_elements(By.XPATH, "//* /section/main/div/div[1]/div/div[1]/div/div/div/div/div/div[1]/div[1]/img")
            
            image_url = image[0].get_attribute("src") # 사진 이미지 url
            insta_image_id = image_url.split('_n.jpg')[0].split('/')[-1].split('_')[-1] # id : 인스타 이미지 고유 id
        

            # 인스타 게시물 정보(셀럽명, 상품명, 브랜드명을 가져옴)


            text = driver.find_elements(By.XPATH, "//* /div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div/span/div/span")[0].text
            insta_celeb = text.split('WHO. ')[1].split('\n')[0]    # 인스타 셀럽 정보 (이름, 그룹명)
            insta_product_brand = text.split('WHAT. ')[1].split('\n')[0]   # 인스타 상품 브랜드명
            insta_product_name = text.split('PRODUCT. ')[1].split('\n')[0] # 인스타 상품명 

            # 셀럽 인스타 url
            celeb_insta_url = ''
            insta_tag_list = driver.find_elements(By.XPATH, "//* /section/main/div/div[1]/div/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div/span/div/span/a")

            for insta_tag in insta_tag_list:
                if insta_tag.text[0] == '@':
                    celeb_insta_url = insta_tag.get_attribute("href")
                    
            # 인스타 댓글에 인스타정보가 없을 경우 패스
            if not celeb_insta_url:
                return
                
            insta_product_category = self.naver_shopping(insta_product_name, driver) # 인스타 상품 카테고리
            


            
            # 셀럽 인스타 url
            driver.get(celeb_insta_url) # 해당 페이지 이동
            driver.implicitly_wait(10)
            
            celeb_insta_id = driver.find_elements(By.XPATH, "//* /div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[1]/a/h2")[0].text
            celeb_follower = driver.find_elements(By.XPATH, "//* /div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span/span")[0].text
            
            
            # db 연결
            conn = pymysql.connect(
                    user="root",
                    password="0000",
                    host="localhost",
                    port=3306,
                    database="style_similar",
                    charset='utf8',

                )

            #저장할 데이터
            celeb_data = (celeb_insta_id, celeb_insta_url, celeb_follower)
            insta_data = (insta_image_id, insta_celeb, insta_product_name, insta_product_brand, insta_product_category, insta_url, celeb_insta_id)
            

            # db에 저장
            with conn.cursor() as cursor:
                sql = "INSERT IGNORE INTO board_celeb (celeb_insta_id, celeb_insta_url, celeb_follower) VALUES (%s, %s, %s)"
                cursor.execute(sql, celeb_data)
                
                sql = "INSERT IGNORE INTO board_insta (insta_image_id, insta_celeb, insta_product_name, insta_product_brand, insta_product_category, insta_url, celeb_insta_id_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, insta_data)


                conn.commit()

            conn.close()   # 연결 닫기

            # 이미지 저장
            urlretrieve(image_url, path_folder + f'{insta_image_id}.jpg')

            
        except Exception as e:
            print(e)
            # 인스타에 1개 사진이 아닌 여러 사진이 있을 때
            # 셀럽의 인스타 주소가 없을 때
            # 네이버 상품이 검색되지 않을 때


    def main(self):
        # 크롬 드라이버 생성
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # 로그인 함수 실행
        id = "qkrgksruf48@gmail.com"
        pw = "wjswkrhd17!"
        self.login(id,pw, driver)

        # 인스타 사진을 가져올 계정 url
        url = "https://www.instagram.com/k_fashion.trend/"
        # 인스타 사진을 저장할 폴더 생성
        path_folder = './static/images/insta/'
        # url에서 각 게시물의 url을 저장
        url_list = self.insta_url(url, path_folder, driver)


        # 인스타 계정 안의 게시물 url들을 모두 가져와 각 게시물의 사진, 메타정보를 저장
        for url in url_list:
            self.insta_data(url, path_folder, driver)

if __name__ == "__main__":
    insta_crawler = InstaCrawling()
    insta_crawler.main()