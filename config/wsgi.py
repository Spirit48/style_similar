"""
WSGI config for ver4_24 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os # 운영체제에서 제공되는 여러 기능을 파이썬에서 수행시켜주는 파이썬 라이브러리(모듈)

from django.core.wsgi import get_wsgi_application

# os.environ 는 운영체제에 등록되어 있는 환경변수에 접근하는 명령어로 os.environ.setdefault(A, B) 는 A라는 이름으로 B를 값으로 등록하겠다는 의미
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# wsgi는 웹 서버 소프트웨어와 파이썬으로 만든 웹 응용 프로그램 간의 표준 인터페이스로 WSGI 규격을 따라 호출 가능한 application 객체를 정의. 웹 서버는 이 application 객체를 호출하여 장고의 애플리케이션을 실행하며 운영 웹 서버와 runserver에서 사용
application = get_wsgi_application()
