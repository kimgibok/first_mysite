# polls 폴더에 urls.py가 없어서 새로 생성
from django.urls import path

from . import views

# 아무것도 없는 주소로 들어가면 views.py에 index함수에 연결
urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.cafe_menu, name="etc.."),
    path("waiting", views.cafe_waiting, name="cafe_waiting"),
    path("review", views.cafe_review, name="cafe_review"),
]