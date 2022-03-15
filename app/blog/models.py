from enum import unique
import os
from re import T
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from jalali_date import datetime2jalali
from comments.models import Comment
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class ArticleManagers(models.Manager):
    def published(self):
        return self.filter(status="P")


class CategoryManagers(models.Manager):
    def active(self):
        return self.filter(status=True)


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.png']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class Article(models.Model):
    STATUS_CHOICES = (
        ('P', 'Published'),
        ('D', 'Draft'),
    )
    title = models.CharField(max_length=128, null=False,
                             blank=False, verbose_name="عنوان")
    content = RichTextUploadingField(verbose_name="متن")
    cover = models.ImageField(upload_to='images/article/%Y/%m/%d/')
    promote = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True,
                            default="", verbose_name="لينك")
    created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="تاريخ ساخت")
    updated = models.DateTimeField(auto_now=True, verbose_name="تاريخ تغيير")
    publish = models.DateTimeField(
        default=timezone.now, verbose_name="تاريخ انتشار")
    category = models.ManyToManyField(
        'Category', verbose_name="دسته بندي", related_name="articles")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="نويسنده", related_name="articles")
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="d", verbose_name="وضعيت")
    objects = ArticleManagers()
    comments = GenericRelation(Comment)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='article_liked',
                                        blank=True)

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def get_jalali(self):
        return datetime2jalali(self.publish).strftime('%y/%m/%d تاريخ _ %H:%M:%S ساعت')

    def active_categories(self):
        return self.category.filter(status=True)
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, unique=True)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ('-publish',)

    def thumbnail_tag(self):
        return format_html("<img width=100 height=100 style='border-radius:5px' src='{}'>".format(self.cover.url))
    thumbnail_tag.short_description = "تصویر مقاله "

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=128, null=False,
                             blank=False, verbose_name="عنوان")
    cover = models.ImageField(upload_to='images/category/%Y/%m/%d/')
    slug = models.SlugField(max_length=100, unique=True,
                            default="", verbose_name="لينك")
    status = models.BooleanField(default=True, verbose_name="نمايش داده شود ؟")
    description = models.CharField(
        max_length=512, null=False, blank=False, default="", verbose_name="توضيحات")
    parent = models.ForeignKey('self', default=None, blank=True, null=True, related_name="children",
                               on_delete=models.SET_NULL, verbose_name="زیر دسته")
    objects = CategoryManagers()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category', args=[self.slug])

    class Meta:
        verbose_name = 'دسته بندي'
        verbose_name_plural = 'دسته بندي ها'
        ordering = ['parent__id']

    def __str__(self):
        return self.title
