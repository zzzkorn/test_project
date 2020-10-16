from django.db import models

from interviewapp.models import Interview
from test_project import settings


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, verbose_name='Пройденый опрос')
    add_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Индексирование
        indexes = [
            models.Index(fields=['user']),
        ]
