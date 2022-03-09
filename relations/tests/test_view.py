import re
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from relations.models import Contact
from django.urls import reverse
User = get_user_model()


class RelationViewTest(TestCase):
    def setUp(self):
        # Create two users
        self.test_user1 = User.objects.create_user(
            username='testuser1', email='example1@gmail.com', phone_number='111', password='1X<ISRUkw+tuK')
        self.test_user2 = User.objects.create_user(
            username='testuser2', email='example2@gmail.com', phone_number='222', password='2HJ1vRV0Z&3iD')

        self.test_user1.save()
        self.test_user2.save()

        self.client = Client()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('relations:user_follow'))
        self.assertRedirects(response, '/account/login/?next=/users/follow/')

    def test_follow_view(self):

        initial_data = {
            'id': 1,
            'action': "follow",

        }
        header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        self.client.login(email='example1@gmail.com', password="1X<ISRUkw+tuK")

        resp = self.client.post("/users/follow/", initial_data, **header)

        self.assertJSONEqual(resp.content, {'status': 'ok'})

        resp = self.client.post("/users/follow/", {'id': 5}, **header)

        self.assertJSONEqual(resp.content, {'status': 'error'})
        resp = self.client.post(
            "/users/follow/", {'id': 5, 'action': 'unfollow'}, **header)

        self.assertJSONEqual(resp.content, {'status': 'error'})
        resp = self.client.post(
            "/users/follow/", {'id': 2, 'action': 'unfollow'}, **header)

        self.assertJSONEqual(resp.content,  {'status': 'ok'})
