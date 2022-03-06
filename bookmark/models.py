from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from jalali_date import datetime2jalali
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericRelation
from comments.models import Comment



class ImageBookmark(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='bookmarks',on_delete=models.CASCADE, verbose_name="کاربر")
    title = models.CharField(max_length=200,verbose_name="عنوان")
    slug = models.SlugField(max_length=200,
                            blank=True)
    url = models.URLField()
    comments = GenericRelation(Comment)
    image = models.ImageField(upload_to='images/bookmark/%Y/%m/%d/')
    description = RichTextField(verbose_name="متن", blank=True)
    created = models.DateField(auto_now_add=True,db_index=True, verbose_name="تاریخ ایجاد")
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='image_liked',
                                        blank=True)

    def __str__(self):
        return self.title

    def get_jalali(self):
        return datetime2jalali(self.created).strftime('%y/%m/%d تاريخ _ %H:%M:%S ساعت')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('bookmark:detail', args=[self.created.year,self.created.month,self.created.day, self.slug, self.id])
    
    def thumbnail_tag(self):
            return format_html("<img width=100 height=100 style='border-radius:5px' src='{}'>".format(self.image.url))
    thumbnail_tag.short_description="تصویر بوكمارك "
    
    class Meta:
        verbose_name = 'بوکمارک'
        verbose_name_plural = 'بوکمارک ها '
        ordering = ('-created',)
    