from django.db import models
import datetime
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have valid username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(verbose_name='Username', max_length=255, unique=True,)
    fullname = models.CharField(verbose_name='Full Name', max_length=255,)
    email = models.EmailField(verbose_name='Email address', max_length=255, unique=True,)
    login_attempts = models.IntegerField(verbose_name='No. of failed attempted logins', default=0, )
    blocked_time = models.DateTimeField(
        verbose_name='Duration till which user is temporarily blocked',
        default=datetime.datetime.now() + datetime.timedelta(minutes=10),
    )
    password_expiry = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(minutes=20),)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def full_name(self):
        return self.fullname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin