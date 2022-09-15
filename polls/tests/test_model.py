from .base import create_question
from django.test import TestCase

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
