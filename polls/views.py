"""View for polls application."""

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Question, Choice


class IndexView(generic.ListView):
    """View for index.html."""

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
    """View for Detail.html."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.localtime())

    def get(self, request, *args, **kwargs):
        """Override the get method to check if the question can be voted.

        Arguments:
            request {HTTP_Request} -- httprequest

        Returns:
            httpresponse -- response of the request
        """
        error = None
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            error = '404'
        # if question is expired show a error and redirect to index
        if error == '404' or not question.can_vote():
            messages.error(
                request, "This question is not available for voting.")
            return HttpResponseRedirect(reverse('polls:index'))
        # go to polls detail application
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    """View for result.html."""

    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Voting for voting button."""
    # get the question or throw error
    question = get_object_or_404(Question, pk=question_id)
    try:
        # if user didnt select a choice or invalid choice
        # it will render as didnt select a choice
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        # if question can vote it will give you
        # to vote it and save the result
        if question.can_vote():
            selected_choice.votes += 1
            selected_choice.save()
            # after voting it will redirct you to result page
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        else:
            # if question is expired it will redirect you to the index page.
            messages.error(request, "You can't vote this question.")
            return HttpResponseRedirect(reverse('polls:index'))
