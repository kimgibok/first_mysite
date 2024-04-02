# polls 폴더에 urls.py가 없어서 새로 생성
from django.urls import path

from . import views

# 아무것도 없는 주소로 들어가면 views.py에 index함수에 연결
app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]