"""
URL configuration for ver4_24 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # include 메소드 추가
from django.http import HttpResponse # http request에 대한 응답 처리 메소드
from django.shortcuts import render # html을 활용하여 response를 생성하는 메소드

# def main(request):
#     return render(request, 'main.html') # 단일 index.html 경우 앱을 생성하지 않고 선언하여 호출

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', main, name='main'),
    path('', include('contents.urls')),
    # path('contents/', include("contents.urls")), # contents 앱 urls 별도 관리, contents 앱에 urls.py 생성 후 runserver 실행
]
