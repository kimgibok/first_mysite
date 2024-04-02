from django.http import HttpResponse, Http404 , HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice

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

# 연습문제
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     choice_list = question.choice_set.all()
#     return render(request, "polls/detail.html", {"detail": choice_list})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question_list = Question.objects.all
    choice = question.choice_set.all
    context={
        "question": question,
        "question_list" : question_list,
        "choice" : choice
    }
    return render(request, "polls/detail.html", context)

def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

from django.db.models import F
def vote(request, question_id):
    # choice 데이터에서 해당하는 값에 votes를 1 더하기
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

