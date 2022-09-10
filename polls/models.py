import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended', null=True)

    @admin.display(
        boolean=True,
        ordering=['pub_date', 'end_date'],
        description='Published recently?',
    )
    def was_published_recently(self):
        return timezone.localtime() >= self.pub_date >= timezone.localtime() - datetime.timedelta(days=1)

    def is_published(self):
        return timezone.localtime() >= self.pub_date

    def can_vote(self):
        if self.end_date:
            return self.is_published and timezone.localtime() <= self.end_date
        return self.is_published()

    def __str__(self) -> str:
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.choice_text
