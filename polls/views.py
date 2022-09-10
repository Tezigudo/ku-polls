from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.localtime()
                                       ).order_by('-pub_date')[:5]


def showtime(request) -> HttpResponse:
    """Return the local time and date."""
    thaitime = timezone.localtime()
    msg = f"<p>The time is {thaitime}.</p>"
    # return the msg in an HTTP response
    return HttpResponse(msg)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.localtime())

    def get(self, request, *args, **kwargs):
        """Override the get method to check if the question can be voted."""
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if not question.can_vote():
            messages.error(
                request, "This question is not available for voting.")
            return HttpResponseRedirect(reverse('polls:index'))
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        if question.can_vote():
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        else:
            messages.error(request, "You can't vote this question.")
            return HttpResponseRedirect(reverse('polls:index'))
