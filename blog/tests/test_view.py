from django.test import TestCase
from django.urls import reverse
import datetime
from blog.models import Article, Category
from django.contrib.auth import get_user_model
from django.core.files import File

User = get_user_model()


class articleiewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        test_user1 = User.objects.create_user(
            username='testuser1', email='example1@gmail.com', phone_number='111', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', email='example2@gmail.com', phone_number='222', password='2HJ1vRV0Z&3iD')
        test_user1.save()
        test_user2.save()

        test_cat1 = Category.objects.create(title="movies", cover=File(open('blog/tests/sample/sample.jpg', "rb")),
                                            status=True, description="test")

        number_of_articles = 13

        for article_id in range(number_of_articles):
            article = Article.objects.create(title=f"test{article_id}",
                                             author=test_user1 if article_id % 2 else test_user2, content=f"test{article_id}", cover=File(open('blog/tests/sample/sample.jpg', "rb")),
                                             promote=True, status="P", slug=f"test{article_id}")
            article.category.add(test_cat1)
            article.save()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/category/movies/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        self.client.login(email='example1@gmail.com', password='1X<ISRUkw+tuK')
        response = self.client.get('/articles/testuser1/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('blog:category', kwargs={'slug': 'movies'}))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='example1@gmail.com', password='1X<ISRUkw+tuK')
        response = self.client.get(
            reverse('blog:user-articles', kwargs={'username': 'testuser1'}))
        self.assertEqual(response.status_code, 200)

    def test_pagination(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['articles']), 4)

        response = self.client.get(
            reverse('blog:category', kwargs={'slug': 'movies'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['articles']), 12)

        self.client.login(email='example1@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.get(
            reverse('blog:user-articles', kwargs={'username': 'testuser1'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['articles']), 5)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('blog:article-edit', kwargs={'pk': 3}))
        self.assertRedirects(
            response, '/account/login/?next=/articles/edit/3/')

    def test_lists_all_articels(self):
        response = self.client.get(reverse('blog:index')+'?page=4')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['articles']), 1)

        response = self.client.get(
            reverse('blog:category', kwargs={'slug': 'movies'})+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['articles']), 1)

        self.client.login(email='example1@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.get(
            reverse('blog:user-articles', kwargs={'username': 'testuser1'})+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['articles']), 1)

    def test_update_article(self):
        response = self.client.get(
            reverse('blog:article-edit', kwargs={'pk': 4}))
        self.assertRedirects(
            response, '/account/login/?next=/articles/edit/4/')

        self.client.login(email='example2@gmail.com', password='2HJ1vRV0Z&3iD')
        initial_data = {
            'title': "moel",
            'content': "test",
            'category': 1,
            'status': 'P',
        }
        resp = self.client.post("/articles/edit/4/", initial_data)
        self.assertEqual(resp.status_code, 403)

        self.client.login(email='example1@gmail.com', password='1X<ISRUkw+tuK')
        resp = self.client.post("/articles/edit/2/", initial_data)
        article = Article.objects.get(pk=2)

        self.assertEqual(article.title, "moel")

    def test_delete_article(self):

        response = self.client.get(
            reverse('blog:article-delete', kwargs={'pk': 1}))
        self.assertRedirects(
            response, '/account/login/?next=/articles/delete/1/')
        self.client.login(email='example2@gmail.com', password='2HJ1vRV0Z&3iD')
        response = self.client.post(
            reverse('blog:article-delete', kwargs={'pk': 4}))
        self.assertEqual(response.status_code, 403)
        self.client.login(email='example1@gmail.com', password='1X<ISRUkw+tuK')
        response = self.client.post(
            reverse('blog:article-delete', kwargs={'pk': 4}))
        self.assertRedirects(response, reverse('blog:index'))
        self.assertFalse(Article.objects.filter(pk=4).exists())

    def test_detail_article(self):
        today = datetime.date.today()
        response = self.client.get(
            reverse('blog:article_detail', kwargs={'year': today.year,
                                                   'month': today.month,
                                                   'day': today.day,
                                                   'slug':  'test1',
                                                   }))
        self.assertEqual(response.status_code, 200)

    def test_like_view(self):

        initial_data = {
            'id': 1,
            'action': "like",

        }
        header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        self.client.login(email='example1@gmail.com', password="1X<ISRUkw+tuK")

        resp = self.client.post("/article/like/", initial_data, **header)

        self.assertJSONEqual(resp.content, {'status': 'ok'})

        resp = self.client.post("/article/like/", {'id': 5}, **header)

        self.assertJSONEqual(resp.content, {'status': 'error'})
        resp = self.client.post(
            "/article/like/", {'id': 50, 'action': 'unlike'}, **header)

        self.assertJSONEqual(resp.content, {'status': 'error'})
        resp = self.client.post(
            "/article/like/", {'id': 2, 'action': 'unlike'}, **header)

        self.assertJSONEqual(resp.content,  {'status': 'ok'})
