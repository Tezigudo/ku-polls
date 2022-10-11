import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from ..models import Vote
from .base import create_question


class VotingTest(TestCase):
    def setUp(self) -> None:
        """Initialize attribute before test"""
        self.user = User.objects.create_user(username="banana01")
        self.user.set_password("apple")
        self.user.save()
        self.client.login(username="banana01", password="apple")

    def test_can_vote_with_future_question(self):
        """
        can_vote() returns False for questions whose pub_date
        is in the future.
        """

        future_ques = create_question("", days=30)
        self.assertIs(future_ques.can_vote(), False)

    def test_can_vote_with_old_question(self):
        """
        can_vote() returns True for old question which not have end_date
        """

        old_question = create_question("", days=-1, seconds=-1)
        self.assertIs(old_question.can_vote(), True)

    def test_can_vote_expired_queston(self):
        """
        can_vote() returns False for expired question
        """

        expired_question = create_question("", days=-1, seconds=1, minutes=1)
        expired_question.end_date = timezone.localtime() - datetime.timedelta(days=1)
        self.assertIs(expired_question.can_vote(), False)

    def test_can_vote_current_time_equal_to_published_date(self):
        """
        voting allow for question which published now
        """

        current_question = create_question("")
        self.assertIs(current_question.can_vote(), True)

    def test_can_vote_current_time_equal_to_expired_time(self):
        """
        voting allowed for question which expired now
        """

        current_question = create_question("", seconds=1)
        current_question.end_date = timezone.localtime() + datetime.timedelta(seconds=1)
        self.assertIs(current_question.can_vote(), True)

    def test_vote_count(self):
        """checl that votes count correctly"""
        ques = create_question("test", days=-1, seconds=-1)
        ch = ques.choice_set.create(choice_text="Yep")
        Vote.objects.create(question=ques, choice=ch, user=self.user)
        self.assertEqual(1, ch.votes)

    def test_authenticated_user_can_vote(self):
        """check that unauthentidated vote will redirected and authenticated user can vote"""
        ques = create_question("test", days=-1, seconds=-1)
        res1 = self.client.post(reverse("polls:vote", args=(ques.id,)))
        self.assertEqual(res1.status_code, 200)
        self.client.logout()
        res2 = self.client.post(reverse("polls:vote", args=(ques.id,)))
        self.assertEqual(res2.status_code, 302)

    def test_one_vote_each_question_and_user(self):
        """one user is one vote for each question"""
        ques = create_question("test", days=-1, seconds=-1)
        ch1 = ques.choice_set.create(choice_text="yes")
        ch2 = ques.choice_set.create(choice_text="no")
        self.client.post(reverse("polls:vote", args=(ques.id,)), {"choice": ch1.id})
        self.assertEqual(ques.vote_set.get(user=self.user).choice, ch1)
        self.assertEqual(Vote.objects.all().count(), 1)
        self.client.post(reverse("polls:vote", args=(ques.id,)), {"choice": ch2.id})
        self.assertEqual(ques.vote_set.get(user=self.user).choice, ch2)
        self.assertEqual(Vote.objects.all().count(), 1)

    def test_not_stealing_vote_for_another_question(self):
        """one user is one vote for each question"""
        ques1 = create_question("test1", days=-1, seconds=-1)
        ques2 = create_question("test2", days=-1, seconds=-1)
        ch1 = ques1.choice_set.create(choice_text="yes")
        ch2 = ques2.choice_set.create(choice_text="no")
        self.client.post(reverse("polls:vote", args=(ques1.id,)), {"choice": ch1.id})
        self.assertEqual(ques1.vote_set.get(user=self.user).choice, ch1)
        self.assertEqual(Vote.objects.all().count(), 1)
        self.client.post(reverse("polls:vote", args=(ques2.id,)), {"choice": ch2.id})
        self.assertEqual(ques2.vote_set.get(user=self.user).choice, ch2)
        self.assertEqual(Vote.objects.all().count(), 2)
