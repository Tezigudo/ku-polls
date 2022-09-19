from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .base import create_question


class QuestionDetailViewTests(TestCase):

    def setUp(self) -> None:
        """ Initialize attribute before test"""
        self.user = User.objects.create_user(username='banana01')
        self.user.set_password('apple')
        self.user.save()
        self.client.login(username='banana01', password='apple')

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 redirected (unpublished question)
        """
        future_question = create_question(
            question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        # if polls arent open it will reqirect(maybe) or
        # 302 redirect i dont sure this one
        self.assertEqual(response.status_code, 302)

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

    def test_visiblity(self):
        """any one should see polls index pages"""
        self.client.logout()
        res = self.client.get(reverse('polls:index'))
        self.assertEqual(res.status_code, 200)

