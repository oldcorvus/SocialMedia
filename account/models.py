from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_jalali.db import models as jmodels
from .managers import UserManager
from .utils import get_random_str

def upload_location(instance, filename):
    return f"user_profiles/{instance.username.lower()}/{get_random_str(10, 50)}.jpg"

class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, unique=True, db_index=True,
                                verbose_name="نام کاربری")
    first_name = models.CharField(max_length=20,
                                  verbose_name="نام", blank=True)
    last_name = models.CharField(max_length=30,
                                 verbose_name="نام خانوادگی", blank=True)
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, verbose_name="ایمیل شما")
    date_joined = jmodels.jDateTimeField("تاریخ عضویت", default=timezone.now)
    profile_image = models.ImageField(upload_to=upload_location, verbose_name="عکس پروفایل",
                                      null=True, blank=True)
    about_me = models.TextField(max_length=150,
                                verbose_name="درباره من", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'پروفايل كاربر'
        verbose_name_plural = 'پروفايل كاربرها'

    def __str__(self):
        return self.username

    @property
    def get_name_or_username(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'
