from django.db import models

from authapp.models import RespondentUser


class Interview(models.Model):
    name = models.CharField(max_length=300, verbose_name='Имя опроса')
    start_date = models.DateTimeField(auto_now_add=True, verbose_name='Время старта опроса')
    expiration_date = models.DateTimeField(verbose_name='Время окончания опроса')
    description = models.TextField(verbose_name='Описание опроса')
    is_active = models.BooleanField(verbose_name='Опрос активен', default=True)

    class Meta:
        # Индексирование
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f'{self.name}. Количество вопросов: {self.number_of_questions}'

    @property
    def number_of_questions(self):
        return len(Question.objects.filter(is_active=True, inside_interview=self))


class Question(models.Model):
    inside_interview = models.ForeignKey(Interview, on_delete=models.CASCADE,
                                         verbose_name='К какому опросу относится вопрос')
    question_text = models.TextField(verbose_name='Текст опроса')
    ResponseType = models.TextChoices('ResponseType', 'text one_variant several_variants')
    response_type = models.CharField(max_length=20, choices=ResponseType.choices, default=ResponseType.one_variant,
                                     verbose_name='Тип ответа')
    is_active = models.BooleanField(verbose_name='Вопрос активен', default=True)

    class Meta:
        indexes = [
            models.Index(fields=['inside_interview']),
            models.Index(fields=['is_active'])
        ]


class Response(models.Model):
    interviewee = models.ForeignKey(RespondentUser, on_delete=models.CASCADE, verbose_name='Интервьюируемый',
                                    blank=True, null=True, related_name='interviewee')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='question')
    response_time = models.DateTimeField(auto_now_add=True, verbose_name='Время ответа')
    response_data = models.TextField(verbose_name='Информация об ответе в JSON формате')

    class Meta:
        # Индексирование
        indexes = [
            models.Index(fields=['interviewee']),
            models.Index(fields=['question'])
        ]
