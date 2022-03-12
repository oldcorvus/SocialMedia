from comments.models import Comment
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from bookmark.models import ImageBookmark
User = get_user_model()


class CommentViewTest(TestCase):
    def setUp(self):
        # Create user
        self.test_user1 = User.objects.create_user(
            username='testuser1', email='example1@gmail.com', phone_number='111', password='1X<ISRUkw+tuK')

        self.test_user1.save()
        self.client = Client()

        self.bookmark = ImageBookmark.objects.create(title="test", author=self.test_user1, description="test",url="sample.com")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('comments:add-comment',kwargs={"type": 'article',
        "id": 1}))
        self.assertRedirects(response, '/account/login/?next=/comments/article/1/')

    def test_comment_view(self):


        self.client.login(email='example1@gmail.com', password="1X<ISRUkw+tuK")

        resp = self.client.post("/comments/article/40",)

        self.assertEqual(resp.status_code, 301)
        initial_data = {
            'body': "test_comment_body",

        }
        resp = self.client.post("/comments/bookmark/1/",initial_data)
        self.assertTrue(Comment.objects.get(pk=1))

        self.client.login(email='example1@gmail.com', password="1X<ISRUkw+tuK")

        initial_data = {
            'body': "test_reply_body",
        }

        resp = self.client.post("/comments/bookmark/1/1/",initial_data)
        self.assertTrue(Comment.objects.get(pk=2))
        self.assertTrue(Comment.objects.get(pk=2).is_reply)
        self.assertEqual(Comment.objects.get(pk=2).reply, Comment.objects.get(pk=1))




     

        