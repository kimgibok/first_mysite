from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def cafe_menu(request):
    return HttpResponse("메뉴가 많아요")
def cafe_review(request):
    return HttpResponse("맛있게 드셨나요! 후기 부탁드려요")
def cafe_waiting(request):
    return HttpResponse("잠시만 기다려주세요 금방 드릴게요")

