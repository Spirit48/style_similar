# pip install beautifulsoup4
# pip install pandas
# pip install requests
# pip install pymysql


import bs4
from bs4 import BeautifulSoup
import pandas as pd
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


    def goods_data(self, mall_category, url):

        self.url = url
        self.mall_category = mall_category

        # category_folder 폴더가 없을경우 폴더 생성
        path_folder = f"../static/images/musinsa/{mall_category}" 
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

                    if name_text[:2] == '제작':
                        # 필요없는 텍스트 삭제 (EX : 제작 14일         포켓 드레스 ...)
                        name_text = name_text.replace(name_text[:10], '').strip()                       

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
                try:
                    for link in range(len(href_list)):
                        product_number = href_list[link].split("/")[-1]
                        urlretrieve(img_link[link], os.path.join(path_folder, f'{product_number}.jpg'))

                    print(f"{mall_category} {page}페이지 이미지 다운로드 완료")
                except:
                    continue

                df = pd.DataFrame(zip(brand_list, name_list, href_list, price_list), columns = ['mall_brand', 'mall_name', 'mall_url', 'mall_price'])
                df['mall_image_id'] = df['mall_url'].str.extract(r'/goods/(\d+)')
                
                df['mall_category'] = mall_category

                new_order = ['mall_image_id', 'mall_name', 'mall_brand', 'mall_price', 'mall_url', 'mall_category']
                df = df[new_order]

                # db 연결
                conn = pymysql.connect(
                        user="style_similar",
                        password="tmxkdlftlalffj9446!!",
                        host="192.168.0.100",
                        port=3306,
                        database="style_similar",
                        charset='utf8',
                    )

                # DataFrame을 리스트로 변환
                data_to_insert = df.values.tolist()

                # db에 저장
                with conn.cursor() as cursor:
                    for data in data_to_insert:
                        sql = "INSERT IGNORE INTO contents_mall (mall_image_id, mall_name, mall_brand, mall_price, mall_url, mall_category_id) VALUES (%s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, data)
                        conn.commit()

                conn.close()   # 연결 닫기


            else:
                print(f"{mall_category} {page}페이지 불러오기 안됨")


            
                


    def category_dataset(self):
        conn = pymysql.connect(
            user="style_similar",
            password="tmxkdlftlalffj9446!!",
            host="192.168.0.100",
            port=3306,
            database="style_similar",
            charset='utf8',
        )

        # db에 저장
        with conn.cursor() as cursor:
            sql_query = "SELECT mall_category, mall_category_url FROM contents_category LIMIT 0, 5" 
            cursor.execute(sql_query)
            # 결과 가져오기
            category_list = cursor.fetchall()

        conn.close()   # 연결 닫기
        
        return category_list


    def main(self):

        category_list = self.category_dataset()

        for mall_category, url in category_list:
            # 클래스의 메서드로 변경한 goods_data 메서드를 호출
            self.goods_data(mall_category, url)


if __name__ == "__main__":
    crawling = GoodsCrawling()  # 클래스의 인스턴스 생성
    crawling.main()