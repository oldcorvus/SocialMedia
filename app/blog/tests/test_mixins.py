from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Category, Article
from django.core.files import File

User = get_user_model()


class MixinsTest(TestCase):
    def setUp(self):
        # Create two users
        self.test_user1 = User.objects.create_user(
            username='testuser1', email='example1@gmail.com', phone_number='111', password='1X<ISRUkw+tuK')
        self.test_user2 = User.objects.create_user(
            username='testuser2', email='example2@gmail.com', phone_number='222', password='2HJ1vRV0Z&3iD')

    def test_author_mixin(self):
        forbidden_status, success_status = 403, 200
        self.client.login(email='example1@gmail.com', password='1X<ISRUkw+tuK')
        req = self.client.get("/account/profile/edit/2/")
        self.assertEqual(req.status_code, forbidden_status)
        req = self.client.get("/account/profile/edit/1/")
        self.assertEqual(req.status_code, success_status)

    def test_ajax_required_mixin(self):
        badrequest_status, success_status = 400, 200

        test_cat1 = Category.objects.create(title="movies", cover=File(open('blog/tests/sample/sample.jpg', "rb")),
                                            status=True, description="test")
        article = Article.objects.create(title="test", author=self.test_user1, content="test", cover=File(open('blog/tests/sample/sample.jpg', "rb")),
                                         promote=True, status="P", slug="test")
        article.category.add(test_cat1)
        article.save()

        initial_data = {
            'id': 1,
            'action': "like",

        }
        header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        self.client.login(email='example1@gmail.com', password="1X<ISRUkw+tuK")

        resp = self.client.post("/article/like/", initial_data, **header)

        self.assertEqual(resp.status_code, success_status)
        resp = self.client.post("/article/like/", initial_data)
        self.assertEqual(resp.status_code, badrequest_status)
