#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os # 운영체제에서 제공되는 여러 기능을 파이썬에서 수행할 수 있게 해줍니다.
import sys # 파이썬 인터프리터를 제어하는데 사용되는 기본 모듈


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
