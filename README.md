# first_mysite

# Django 시작
- git repository 만들어서 git clone -> 만들어진 곳 디렉토리로 들어가서 -> django-admin startproject mysite

- 결과
``` 
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

# 개발서버 
```
python manage.py runserver
```

# 앱 생성하기
- polls앱 생성하기
```
python manage.py startapp polls
```
- 결과 파일

디렉토리에 polls가 생성된다
```
polls/
    migrations/
        __init__.py
    __init__.py
    admin.py
    apps.py
    models.py
    tests.py
    views.py
```

# 첫 번째 뷰 작성하기

