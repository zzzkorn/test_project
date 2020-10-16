from django.contrib.auth.models import AbstractUser
from django.db import models


class RespondentUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True, verbose_name='Аватар')
    age = models.PositiveSmallIntegerField(verbose_name='Возраст')
