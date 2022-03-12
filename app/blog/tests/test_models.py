from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Article, Category
import datetime
from django.core.files import File

User = get_user_model()


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(
            username='testuser1', email='example1@gmail.com', phone_number='111', password='1X<ISRUkw+tuK')
        test_user1.save()
        test_cat1 = Category.objects.create(title="movies", cover=File(open('blog/tests/sample/sample.jpg', "rb")),
                                            status=True, description="test")
        test_cat2 = Category.objects.create(title="books", cover=File(open('blog/tests/sample/sample.jpg', "rb")),
                                            status=False, description="test")
        article = Article.objects.create(title="test", author=test_user1, content="test", cover=File(open('blog/tests/sample/sample.jpg', "rb")),
                                         promote=True, status="P", slug="test")
        article.category.add(test_cat1, test_cat2)
        article.save()

    def test_article_get_absolute_url(self):
        article = Article.objects.get(id=1)
        self.assertEqual(article.get_absolute_url(
        ), f'/articles/{datetime.date.today().year}/{datetime.date.today().month}/{datetime.date.today().day}/test/')

    def test_article_active_category(self):
        article = Article.objects.get(id=1)
        category = Category.objects.get(pk=1)
        self.assertEqual(article.active_categories().count(), 1)
        self.assertEqual(article.active_categories()[0], category)

    def test_category_get_absolute_url(self):
        category = Category.objects.get(id=1)
        self.assertEqual(category.get_absolute_url(), f'/category/movies/')
