from django.db import models

from ckeditor.fields import RichTextField

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

User = get_user_model()


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_comments')
    reply = models.ForeignKey('self', on_delete=models.CASCADE,
                              null=True, blank=True, related_name='reply_comment')
    is_reply = models.BooleanField(default=False)
    body = RichTextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'{self.author} - {self.body[:30]}'

    class Meta:
        ordering = ('-created',)
