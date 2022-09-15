import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ..models import Question


def create_question(question_text, days=0, hours=0,  minutes=0, seconds=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """

    time = timezone.localtime() + datetime.timedelta(days=days, hours=hours,
                                                     minutes=minutes, seconds=seconds)

    return Question.objects.create(question_text=question_text, pub_date=time)






