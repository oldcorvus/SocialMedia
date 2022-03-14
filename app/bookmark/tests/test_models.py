from django.test import TestCase
from bookmark.models import ImageBookmark
from django.contrib.auth import get_user_model
from bookmark.models import ImageBookmark
import datetime

User = get_user_model()

class BookmarkModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='testuser1', email='example1@gmail.com', phone_number='111', password='1X<ISRUkw+tuK')

        test_user1.save()
        bookmark = ImageBookmark.objects.create(title="test", author=test_user1, description="test",url="sample.com")
    
    def test_get_absolute_url(self):
        bookmark = ImageBookmark.objects.get(id=1)
        self.assertEqual(bookmark.get_absolute_url(), f'/bookmark/detail/{datetime.date.today().year}/{datetime.date.today().month}/{datetime.date.today().day}/test/1/')