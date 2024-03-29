from django.http import HttpResponse, Http404 
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.utils import timezone

from .models import Question

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {
#         "likelion": latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))


def index(request):
    today = timezone.now().date()
    latest_question_list = Question.objects.filter(pub_date__lt = today)
    total_question_count = Question.objects.count()
    context = {"likelion": latest_question_list, "totalcount":total_question_count}
    return render(request, "polls/index.html", context)

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choice_list = question.choice_set.all()
    return render(request, "polls/detail.html", {"detail": choice_list})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)



def test1(request):
    question_list = Question.objects.order_by("-pub_date")[:10]
    return HttpResponse(question_list)

def test2(request):
    today = timezone.now().date()
    question_list = Question.objects.filter(pub_date__date=today)
    output = ", ".join([q.question_text for q in question_list])
    return HttpResponse(output)

def test3(request):
    return HttpResponse("Hello, World!")

def test4(request):
    current_year = timezone.now().year
    question_list = Question.objects.filter(pub_date__year=current_year)
    output = "<br>".join([q.question_text for q in question_list])
    return HttpResponse(output)
