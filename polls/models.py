from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    # pub_date = models.DateTimeField(auto_now_add=True) # 알아서 입력되게
    pub_date = models.DateTimeField("pub date") 
    
    # 매직매소드
    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description="Published recently?"
    )
    def was_published_recently(self):
        return self.pub_date >=timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
    
