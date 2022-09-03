from django.http import HttpResponse, Http404
from django.utils import timezone
# from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import Question


def index(request):
    last_question_list = Question.objects.order_by('-pub_date')[:5]
    # template method
    # template = loader.get_template('polls/index.html')
    context = {
        'lastest_question_list': last_question_list
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def showtime(request) -> HttpResponse:
    """Return the local time and date."""
    thaitime = timezone.localtime()
    msg = f"<p>The time is {thaitime}.</p>"
    # return the msg in an HTTP response
    return HttpResponse(msg)


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question doesn't exist")
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    return HttpResponse(f"You're looking result of question {question_id}")


def vote(request, question_id):
    return HttpResponse(f"You're voting at question {question_id}")
