#pip install pandas

import pymysql
import pandas as pd

def add_category_db():

    dataset = [
        ['shirts_blouse', 'https://www.musinsa.com/categories/item/001002', '블라우스/셔츠'],
        ['tshirts', 'https://www.musinsa.com/categories/item/001001', '티셔츠'],
        ['knit_sweater', 'https://www.musinsa.com/categories/item/001006', '니트/스웨터'],
        ['maxi_dress', 'https://www.musinsa.com/categories/item/020008', '원피스'],
        ['sneakers', 'https://www.musinsa.com/categories/item/018003', '스니커즈'],
        ['sports_shoes','https://www.musinsa.com/categories/item/018001', '러닝화'],
        ['shoes', 'https://www.musinsa.com/categories/item/005014', '구두'],
    ]
    category_dataset = pd.DataFrame(dataset, columns=['mall_category','mall_category_url','mall_category_name'])
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
        for _, row in category_dataset.iterrows():  # 데이터프레임의 각 행을 순회합니다.
            data = (row['mall_category'], row['mall_category_url'], row['mall_category_name'])
            sql = "INSERT IGNORE INTO contents_category (mall_category, mall_category_url, mall_category_name) VALUES (%s, %s, %s)"
            cursor.execute(sql, data)
            conn.commit()

    conn.close()   # 연결 닫기


add_category_db()