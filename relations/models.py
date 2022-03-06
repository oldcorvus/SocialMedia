from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Contact(models.Model):
    user_from = models.ForeignKey('account.CustomUser',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('account.CustomUser',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


class Action(models.Model):
    user = models.ForeignKey('account.CustomUser',
                             related_name='actions',
                             db_index=True,
                             on_delete=models.CASCADE, default="")
    verb = models.CharField(max_length=255, default="")
    target_ct = models.ForeignKey(ContentType,
                                  blank=True,
                                  null=True,
                                  related_name='target_obj',
                                  on_delete=models.CASCADE, default="")
    target_id = models.PositiveIntegerField(null=True,
                                            blank=True,
                                            db_index=True, default="")
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)
