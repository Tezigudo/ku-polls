"""Model for polls application."""
import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Model for polls question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended', null=True, blank=True)

    @admin.display(
        boolean=True,
        ordering=['pub_date', 'end_date'],
        description='Published recently?',
    )
    def was_published_recently(self) -> bool:
        """Check whether question was publish less than 1 day or not.

        Returns:
            bool -- True if question was publlish recently, False otherwise
        """
        return timezone.localtime() >= self.pub_date >= timezone.localtime() - datetime.timedelta(days=1)

    def is_published(self) -> bool:
        """Check whether question was published or not by published date and today(time now).

        Returns:
            bool -- True if now time more than publishing date, False otherwise
        """
        return timezone.localtime() >= self.pub_date

    def can_vote(self) -> bool:
        """Check whether question can be voted or not if now time is more than end dated visitor can not vote anymore.

        Returns:
            bool -- True if question are not expired, False otherwise
        """
        # check whether end date is not NULL
        if self.end_date:
            return self.is_published and timezone.localtime() <= self.end_date
        return self.is_published()

    def __str__(self) -> str:
        """Visualize python object using string method.

        Returns:
            str -- polls's question text
        """
        return self.question_text


class Choice(models.Model):
    """Model for choice in polls."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    @property
    def votes(self):
        return Vote.objects.filter(choice=self).count()

    def __str__(self) -> str:
        """Visualize python object using string method.

        Returns:
            str -- polls's choice text
        """
        return self.choice_text


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __repr__(self) -> str:
        return f'Vote(user={self.user.id}, questionid={self.question.id}, choiceid={self.choice.id})'
