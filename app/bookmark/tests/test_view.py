from django.test import TestCase
from django.urls import reverse
import datetime
from bookmark.models import ImageBookmark
from django.contrib.auth import get_user_model
User = get_user_model()


class bookmarkiewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create two users
        test_user1 = User.objects.create_user(
            username='testuser1', email='example1@gmail.com', phone_number='111', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(
            username='testuser2', email='example2@gmail.com', phone_number='222', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        number_of_bookmarks = 13

        for bookmark_id in range(number_of_bookmarks):
            ImageBookmark.objects.create(
                title=f'test{bookmark_id}',
                description=f'test {bookmark_id}',
                url=f'example.com/{bookmark_id}.jpg',
                author=test_user1 if bookmark_id % 2 else test_user2,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/bookmark/list/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('bookmark:list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('bookmark:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookmark/list.html')
        header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        response = self.client.get(reverse('bookmark:list'), **header)
        self.assertTemplateUsed(response, 'bookmark/list_ajax.html')

    def test_pagination(self):
        response = self.client.get(reverse('bookmark:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['images']), 5)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse('bookmark:bookmark-edit', kwargs={'pk': 3}))
        self.assertRedirects(
            response, '/account/login/?next=/bookmark/edit/3/')

    def test_lists_all_bookmarks(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('bookmark:list')+'?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['images']), 3)

    def test_update_bookmark(self):
        response = self.client.get(
            reverse('bookmark:bookmark-edit', kwargs={'pk': 4}))
        self.assertRedirects(
            response, '/account/login/?next=/bookmark/edit/4/')

        self.client.login(email='example2@gmail.com', password='2HJ1vRV0Z&3iD')

        initial_data = {
            'title': "moel",
        }
        resp = self.client.post("/bookmark/edit/4/", initial_data)
        self.assertEqual(resp.status_code, 403)

        self.client.login(email='example1@gmail.com', password='1X<ISRUkw+tuK')
        resp = self.client.post("/bookmark/edit/4/", initial_data)
        bookmark = ImageBookmark.objects.get(pk=4)
        self.assertEqual(bookmark.title, "moel")

    def test_delete_bookmark(self):

        response = self.client.get(
            reverse('bookmark:bookmark-delete', kwargs={'pk': 1}))
        self.assertRedirects(
            response, '/account/login/?next=/bookmark/delete/1/')
        self.client.login(email='example2@gmail.com', password='2HJ1vRV0Z&3iD')
        response = self.client.post(
            reverse('bookmark:bookmark-delete', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 403)
        self.client.login(email='example1@gmail.com', password='1X<ISRUkw+tuK')
        response = self.client.post(
            reverse('bookmark:bookmark-delete', kwargs={'pk': 2}))
        self.assertRedirects(response, reverse('blog:index'))
        self.assertFalse(ImageBookmark.objects.filter(pk = 2).exists())

    def test_detail_bookmark(self):
        today = datetime.date.today()
        response = self.client.get(
            reverse('bookmark:detail', kwargs={'year' : today.year,
                'month' : today.month,
                'day' : today.day,
                'slug' :  'test0',
                'id': 1}))
        self.assertEqual(response.status_code, 200)


    def test_follow_view(self):
    
        initial_data = {
            'id': 1,
            'action': "like",

        }
        header = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        self.client.login(email='example1@gmail.com', password="1X<ISRUkw+tuK")

        resp = self.client.post("/bookmark/like/", initial_data, **header)

        self.assertJSONEqual(resp.content, {'status': 'ok'})

        resp = self.client.post("/bookmark/like/", {'id': 5}, **header)

        self.assertJSONEqual(resp.content, {'status': 'error'})
        resp = self.client.post(
            "/bookmark/like/", {'id': 50, 'action': 'unlike'}, **header)

        self.assertJSONEqual(resp.content, {'status': 'error'})
        resp = self.client.post(
             "/bookmark/like/", {'id': 2, 'action': 'unlike'}, **header)

        self.assertJSONEqual(resp.content,  {'status': 'ok'})

