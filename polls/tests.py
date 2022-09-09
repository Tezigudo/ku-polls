import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days=0, hours=0,  minutes=0, seconds=0):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """

    time = timezone.localtime() + datetime.timedelta(days=days, hours=hours,
                                                     minutes=minutes, seconds=seconds)

    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """

        future_ques = create_question('', days=30)
        self.assertIs(future_ques.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """

        old_question = create_question('', days=1, seconds=1)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """

        recent_question = create_question(
            '', hours=-23, minutes=-59, seconds=-59)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() returns False for questions whose pub_date
        is in the future.
        """

        future_ques = create_question('', days=30)
        self.assertIs(future_ques.is_published(), False)

    def test_is_published_with_old_question(self):
        """
        is_published() returns True for questions whose pub_date
        is older than 1 day.
        """

        old_question = create_question('', days=-1, seconds=-1)
        self.assertIs(old_question.is_published(), True)

    def test_can_vote_with_future_question(self):
        """
        can_vote() returns False for questions whose pub_date
        is in the future.
        """

        future_ques = create_question('', days=30)
        self.assertIs(future_ques.can_vote(), False)

    def test_can_vote_with_old_question(self):
        """
        can_vote() returns True for old question which not have end_date
        """

        old_question = create_question('', days=-1, seconds=-1)
        self.assertIs(old_question.can_vote(), True)

    def test_can_vote_expired_queston(self):
        """
        can_vote() returns False for expired question
        """

        expired_question = create_question(
            '', days=-1, seconds=1, minutes=1)
        expired_question.end_date = timezone.localtime() - \
            datetime.timedelta(days=1)
        self.assertIs(expired_question.can_vote(), False)

    def test_can_vote_current_time_equal_to_published_date(self):
        """
        voting allow for question which published now
        """

        current_question = create_question('')
        self.assertIs(current_question.can_vote(), True)

    def test_can_vote_current_time_equal_to_expired_time(self):
        """
        voting allowed for question which expired now
        """

        current_question = create_question('', seconds=1)
        current_question.end_date = timezone.localtime()+datetime.timedelta(seconds=1)
        self.assertIs(current_question.can_vote(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(
            question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
