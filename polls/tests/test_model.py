from django.test import TestCase

from .base import create_question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """

        future_ques = create_question("", days=30)
        self.assertIs(future_ques.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """

        old_question = create_question("", days=1, seconds=1)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """

        recent_question = create_question("", hours=-23, minutes=-59, seconds=-59)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """
        is_published() returns False for questions whose pub_date
        is in the future.
        """

        future_ques = create_question("", days=30)
        self.assertIs(future_ques.is_published(), False)

    def test_is_published_with_old_question(self):
        """
        is_published() returns True for questions whose pub_date
        is older than 1 day.
        """

        old_question = create_question("", days=-1, seconds=-1)
        self.assertIs(old_question.is_published(), True)
