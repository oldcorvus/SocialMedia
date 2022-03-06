from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, email,  password,  **extra_fields):
        if not phone_number:
            raise ValueError('مقدار شماره تماس نیاز است')

        if not email:
            raise ValueError('مقدار ایمیل نیاز است')

        user = self.model(username=username, phone_number=phone_number,
                          email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _create_user(self, email, password, phone_number, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('مقدار ایمیل نیاز است')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone_number=phone_number,
            is_admin=is_staff,
            is_active=True,
            is_superuser=is_superuser,

            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email,  password, **extra_fields):
        user = self._create_user(
            email, password, phone_number, True, True, **extra_fields)
        return user
