from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse, Http404 , HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.db.models import Sum
from django.urls import reverse_lazy


from .models import Question, Choice

class QuestionDeleteView(generic.edit.DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete.html'
    success_url = reverse_lazy('polls:index') 


class QuestionUpdateView(generic.edit.UpdateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/question_update_form.html'  # 재사용하거나 적절한 템플릿 지정
    success_url = reverse_lazy('polls:index')  # 예시 URL, 실제 프로젝트에 맞게 수정 필요
    
class ChoiceUpdateView(generic.edit.UpdateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_update_form.html'  # 새로운 템플릿 또는 기존 템플릿 지정

    def get_success_url(self):
        # 선택지가 업데이트된 후, 선택지가 속한 질문의 상세 페이지로 리다이렉션
        choice = self.object
        return reverse('polls:detail', kwargs={'q_id': choice.question.pk})


class ChoiceCreateView(generic.edit.CreateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_form.html'
    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)
    success_url = reverse_lazy('polls:index')

class QuestionCreateView(generic.edit.CreateView):
    model = Question
    # fields = ['question_text', 'pub_date'] # pub_date를 자동으로 입력하게 해서
    fields = ['question_text']
    template_name = 'polls/question_form.html'
    success_url = reverse_lazy('polls:index')


# IndexView
class IndexView(generic.ListView):  # generic에서 ListView 상속
    # [app_name]/[model_name]_list.html
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")

    # def get_queryset(self): 
    #     return Question.objects.order_by("-pub_date")
    #     # return Question.objects.annotate(total_votes=Sum('choice__votes')).order_by('-total_votes')[:3]
    #     # return Question.objects.annotate(total_votes=Sum('choice__votes')).filter(total_votes=0)
    #     # return Question.objects.all()
    
    
# DetailView
class DetailView(generic.DetailView):  # generic에서 DetailView상속
    model = Question  # 어떤 질문인지 응답을 해줌 나머지는 상속받음
    # [app_name]/[model_name]_detail.html
    # template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    # def get_object(self):
    #     question_id = self.kwargs['pk']
    #     question = get_object_or_404(Question, pk=question_id)
    #     return question
    


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    def get_object(self):
        # question의 choice가 없으면 페이지 나타내지 않는다.
        question = get_object_or_404(Question, pk=self.kwargs.get('pk'))
        if not question.choice_set.exists():
            raise Http404("No choices found for this question.")
        return question


def index(request):
    today = timezone.now().date()
    latest_question_list = Question.objects.filter(pub_date__lt = today)
    total_question_count = Question.objects.count()
    context = {"likelion": latest_question_list, "totalcount":total_question_count}
    return render(request, "polls/index.html", context)


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

