# polls 폴더에 urls.py가 없어서 새로 생성
from django.urls import path

from . import views

# 아무것도 없는 주소로 들어가면 views.py에 index함수에 연결
app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),  # as_view()를 써줘야 화면에 렌더링이 됨
    # ex: /polls/5/
    path("<int:q_id>/", views.DetailView.as_view(), name="detail"),  # <int:pk> generic은 이미 구조가 짜여저있기 때문에 pk로 설정해 주어야 한다. question_id이런거 못 알아들음
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]