import os
import shutil

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import CustomUser


@receiver(pre_delete, sender=CustomUser)
def delete_user_profile_folder(sender, instance, **kwargs):
    try:
        user_profile_dir_name = os.path.dirname(instance.profile_image.path)
        shutil.rmtree(user_profile_dir_name)
    except ValueError:
        pass
