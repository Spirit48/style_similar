"""
ASGI config for ver4_24 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os # 운영체제에서 제공되는 여러 기능을 파이썬에서 수행시켜주는 파이썬 라이브러리(모듈)

# ASGI는 비동기 서버 게이트웨이 인터페이스(Asynchronous Server Gateway Interface)로 동기 앱과 비동기 앱을 모두 지원하며 오래된 동기 WSGI 웹 앱을 ASGI로 마이그레이션할 수도 있음
from django.core.asgi import get_asgi_application

# os.environ 는 운영체제에 등록되어 있는 환경변수에 접근하는 명령어로 os.environ.setdefault(A, B) 는 A라는 이름으로 B를 값으로 등록하겠다는 의미
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
