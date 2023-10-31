from . import views # 같은 경로에 있는 views.py를 가져오기 위한 import 선언 #
from django.urls import path # 장고 프레임웤 urls 정의된 클래스 import 선언 #

urlpatterns = [
    path('', views.insta_image_list, name='insta_image_list'),
    path('insta_detail/<str:insta_image_id>', views.insta_detail, name='insta_detail'),
    path('product_detail/<str:mall_image_id>', views.product_detail, name='product_detail'),
]

