# 초기설정
- 가상환경 만들어서 새로 시작하기
- conda create -n dj python=3.10
- pip install django

# Django 시작
- git repository 만들어서 git clone -> 만들어진 곳 디렉토리로 들어가서 -> django-admin startproject mysite

- 결과
``` 
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

## 라우팅 
- view 작성

“polls/view.py” 파일에 다음과 같은 코드 입력
```
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def cafe_menu(request):
    return HttpResponse("메뉴가 많아요")
def cafe_review(request):
    return HttpResponse("맛있게 드셨나요! 후기 부탁드려요")
def cafe_waiting(request):
    return HttpResponse("잠시만 기다려주세요 금방 드릴게요")
```

- view 호출하기

뷰를 호출하려면 URL과 연결하여야 한다 -> URLconf가 사용

polls 디렉토리에서 URLconf를 생성하려면 ``urls.py``라는 파일을 생성해야 합니다.

- polls/urls.py생성 

*** mysite/urls.py***와 다르다!!!

polls/urls.py에 다음과 같은 코드 작성
```
# polls 폴더에 urls.py가 없어서 새로 생성
from django.urls import path

from . import views

# 아무것도 없는 주소로 들어가면 views.py에 index함수에 연결
urlpatterns = [
    path("", views.index, name="index"),   # polls의 주소값이 아무것도 없다면 views.index호출해랴 : http://localhost:8000/polls/
    path("menu", views.cafe_menu, name="etc.."), # http://localhost:8000/polls/menu 라면 views.cafe_menu호출
    path("waiting", views.cafe_waiting, name="cafe_waiting"),
    path("review", views.cafe_review, name="cafe_review"),
]
```

- view를 URLconf에 연결

최상위 URLconf 에서 polls.urls 모듈을 바라보게 설정 

mysite/urls.py 파일을 열고, django.urls.include를 import 하고, urlpatterns 리스트에 include() 함수를 다음과 같이 추가

mysite/urls.py에 다음과 같이 입력
 ```
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("polls/", include("polls.urls")),
    path('admin/', admin.site.urls),
]
 ```
 include() 함수는 다른 URLconf들을 참조할 수 있도록 도와줍니다. Django가 함수 include()를 만나게 되면, URL의 그 시점까지 일치하는 부분을 잘라내고, 남은 문자열 부분을 후속 처리를 위해 include 된 URLconf로 전달합니다.
 - 언제 include()를 사용해야 하나요?

다른 URL 패턴을 포함할 때마다 항상 include()를 사용해야 합니다. admin.site.urls가 유일한 예외입니다.

## 데이터베이스

# SQLite database 세팅
- python manage.py migrate -> 자동으로 테이블 생성
- DBeaver -> DB 추가 -> db.sqlite -> 내용 확인

# 테이블 생성
- polls 앱에 models.py 내용을 입력
- settings.py에 app 등록
- python manage.py makemigrations polls -> 설계도 작성
- python manage.py migrate -> table 생성
- 생성된 내용 살펴보기

- polls 앱에 models.py 내용을 입력
```
# polls/models.py
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

- settings.py에 app 등록
```
'polls.apps.PollsConfig'

#결과
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls.apps.PollsConfig',  # settings.py에 app 등록
]
```

- python manage.py makemigrations polls -> 설계도 작성

터미널에 다음과 같이 작성
```
python manage.py makemigrations polls
```

결과 (polls/migrations/0001_initial.py)이 생성되고 0001_initial.py에 설계도가 생성됨
```
polls/
    migrations/
        __init__.py
        0001_initial.py
```
```
# 0001_initial.py
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question')),
            ],
        ),
    ]

```

- python manage.py migrate -> table 생성

터미널에 다음과 같이 입력하면 table이 생성된다.
```
python manage.py migrate
```
![alt text](img/image.png)
다음과 같이 생성된 것을 볼 수 있다