from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
import cv2
import pymysql

# 카테고리명을 입력하면 해당 카테고리의 인스타 이미지들을 이미지유사도를 진행해 similarity 데이터를 db에 저장
category = "sneakers"

def insta_crop(image_path):
    image = cv2.imread(image_path)
    
    height, width = image.shape[:2]
    image = image[:, width // 2:]
    

    # 이미지를 그레이스케일로 변환합니다.
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 이미지 이진화 (흑백으로 변환)
    _, thresholded = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY_INV)

    # 경계를 찾아냅니다.
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 물체를 감싸는 가장 큰 사각형을 찾습니다.
    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    # 물체를 감싸는 사각형 좌표를 가져옵니다.
    x, y, w, h = cv2.boundingRect(max_contour)

    # 물체를 crop합니다.
    cropped_object = image[y:y+h, x:x+w]

    return cropped_object

def process_images_in_folder(input_folder, output_folder):
    # 입력 폴더와 출력 폴더의 경로를 받아옵니다.
    image_files = os.listdir(input_folder)

    for file in image_files:
        # 이미지 파일의 전체 경로를 생성합니다.
        image_path = os.path.join(input_folder, file)

        # 이미지를 crop하여 새로운 이미지를 가져옵니다.
        cropped_object = insta_crop(image_path)

        # 새로운 이미지 파일의 저장 경로를 생성합니다.
        output_path = os.path.join(output_folder, file)

        # crop된 이미지를 새로운 파일로 저장합니다.
        cv2.imwrite(output_path, cropped_object)


# db 연결
conn = pymysql.connect(
        user="style_similar",
        password="tmxkdlftlalffj9446!!",
        host="192.168.0.100",
        port=3306,
        database="style_similar",
        charset='utf8',
    )

# 카테고리명을 가져오고 카테고리명과 일치하는 인스타 이미지들만 선택해서 유사도 진행 
with conn.cursor() as cursor:
            sql1 = f"SELECT mall_category_name FROM contents_category WHERE mall_category = '{category}'"
            cursor.execute(sql1)
            category_name = cursor.fetchone()

            sql2 = f"SELECT insta_image_id FROM contents_insta WHERE insta_product_category = '{category_name[0]}'"
            cursor.execute(sql2)
            insta_image_id_list = cursor.fetchall()
conn.close()


# 폴더 경로를 설정
mall_image_folder = f"../static/images/musinsa/{category}"
insta_input_folder = "../static/images/insta/"
insta_output_folder = "../static/images/insta_product/"

# 출력 폴더가 존재하지 않을 경우 생성합니다.
if not os.path.exists(insta_output_folder):
    os.makedirs(insta_output_folder)

# 이미지 파일들을 crop하여 새로운 이미지 파일로 저장합니다.
process_images_in_folder(insta_input_folder, insta_output_folder)



class FeatureExtractor:
    def __init__(self):
        # 모델 : VGG16, 아키텍처 : imagenet
        base_model = VGG16(weights='imagenet')
        # 모델을 Fully Connected 레이어의 특징을 반환하도록 커스터마이즈합니다.
        self.model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    def extract(self, img):
        # 이미지 리사이징
        img = img.resize((224, 224))
        # 이미지 색상 공간 변환
        img = img.convert('RGB')
        # 이미지 전처리
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # 특징 추출
        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)


# 이미지 데이터베이스 경로 리스트를 가져오는 함수 (getImagePaths 함수가 없는 경우)
def getImagePaths(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(('.jpg', '.jpeg', '.png'))]


# 이미지 데이터베이스 경로 리스트를 가져오는 함수인 getImagePaths를 사용하여 이미지 리스트를 얻습니다.

mall_image_paths = getImagePaths(mall_image_folder)

# FeatureExtractor 클래스를 인스턴스화합니다.
fe = FeatureExtractor()

# 이미지를 순환하다
features = []
for img_path in sorted(mall_image_paths):
    img = Image.open(img_path)
    feature = fe.extract(img)
    features.append(feature)


def process_images_in_folder(input_folder, output_folder):
    # 입력 폴더와 출력 폴더의 경로를 받아옵니다.
    image_files = os.listdir(input_folder)

    for file_name in image_files:
        # 이미지 파일의 전체 경로를 생성합니다.
        image_path = os.path.join(input_folder, file_name)

        # 이미지를 crop하여 새로운 이미지를 가져옵니다.
        cropped_object = insta_crop(image_path)

        # 새로운 이미지 파일의 저장 경로를 생성합니다.
        output_path = os.path.join(output_folder, file_name)

        # crop된 이미지를 새로운 파일로 저장합니다.
        cv2.imwrite(output_path, cropped_object)


# 이미지 데이터베이스 경로 리스트를 가져오는 함수인 getImagePaths를 사용하여 이미지 리스트를 얻습니다.
insta_image_paths = []
for insta_image_id in insta_image_id_list:
    insta_image_paths.append("../static/images/insta_product/"+insta_image_id[0]+".jpg")

# 인스타 상품 이미지 쿼리 삽입
for insta_path in insta_image_paths:
    insta_img = Image.open(insta_path)
    # 인스타 상품 이미지 특징 추출
    query = fe.extract(insta_img)
    # 쇼핑몰 이미지와 인스타 이미지 간의 유사도 측정
    dists = np.linalg.norm(np.array(features) - query, axis=1)
    # 가장 낮은 거리를 가진 30개 이미지 추출
    ids = np.argsort(dists)[:10]
    scores = [(dists[id], mall_image_paths[id]) for id in ids]

    # db 연결
    conn = pymysql.connect(
            user="style_similar",
            password="tmxkdlftlalffj9446!!",
            host="192.168.0.100",
            port=3306,
            database="style_similar",
            charset='utf8',
        )

    # db 저장
    axes = []
    for i in range(10):
        score = scores[i]

        image_path = score[1]  # 이미지 파일 경로 가져오기
        mall_image_id_id = image_path.split('\\')[-1].split('.jpg')[0]
        insta_image_id_id = insta_path.split('/')[-1].split('.jpg')[0]

        similar_distance = "{:.3f}".format(score[0])
        
        data = (similar_distance, insta_image_id_id, mall_image_id_id)
        
        with conn.cursor() as cursor:
            sql = "INSERT IGNORE INTO contents_similarity (similar_distance, insta_image_id_id, mall_image_id_id) VALUES (%s, %s, %s)"
            cursor.execute(sql, data)
            conn.commit()
    print("저장완료")
    conn.close()   # 연결 닫기

