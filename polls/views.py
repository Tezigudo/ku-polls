"""View for polls application."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question, Vote


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
        user = request.user
        try:
            question = get_object_or_404(Question, pk=kwargs['pk'])
        except Http404:
            error = '404'
        # if question is expired show a error and redirect to index
        if error == '404' or not question.can_vote():
            messages.error(
                request, "This question is not available for voting.")
            return HttpResponseRedirect(reverse('polls:index'))
        try:
            if not user.is_authenticated:
                raise Vote.DoesNotExist
            user_vote = question.vote_set.get(user=user).choice
        except Vote.DoesNotExist:
            # if user didnt select a choice or invalid cho[ice
            # it will render as didnt select a choice
            return super().get(request, *args, **kwargs)
        else:
            # go to polls detail application

            return render(request, 'polls/detail.html', {
                'question': question,
                'user_vote': user_vote,
            })


class ResultsView(generic.DetailView):
    """View for result.html."""

    model = Question
    template_name = 'polls/results.html'


@login_required(login_url='/accounts/login')
def vote(request: HttpRequest, question_id):
    """Voting for voting button."""
    # get the question or throw error
    user = request.user
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
            try:
                user_vote = question.vote_set.get(user=user)
                user_vote.choice = selected_choice
                user_vote.save()
            except Vote.DoesNotExist:
                Vote.objects.create(
                    user=user, choice=selected_choice,\
                        question=selected_choice.question).save()
        else:
            # if question is expired it will redirect you to the index page.
            messages.error(request, "You can't vote this question.")
            return HttpResponseRedirect(reverse('polls:index'))

        # after voting it will redirct you to result page
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
