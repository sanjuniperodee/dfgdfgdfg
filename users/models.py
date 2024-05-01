from xml.dom.minidom import Document

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.CharField(max_length=255, unique=True, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=255, unique=True, verbose_name='Номер телефона')
    username = models.CharField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=255, null=True, verbose_name='Пароль')
    user_documents = models.ManyToManyField('Document', blank=True, default=[], verbose_name='Документы')
    apply_approved = models.BooleanField(default=False, verbose_name='')
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    # USERNAME_FIELD = phone_number

    def __str__(self):
        return self.first_name + " " + self.last_name + " : " + str(self.pk)


class UserCreateRequest(models.Model):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.CharField(max_length=255, unique=True, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=255, unique=True, verbose_name='Номер телефона')
    username = models.CharField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=255, null=True, verbose_name='Пароль')
    sms_code = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        verbose_name = 'Запрос на регистрацию'
        verbose_name_plural = 'Запросы на регистрацию'

    # USERNAME_FIELD = phone_number

    def __str__(self):
        return self.first_name + " " + self.last_name + " : " + str(self.pk)


class Type(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название документа')
    score = models.IntegerField(default=0, help_text="Score based on the document's importance.")
    required = models.BooleanField(default=False)
    def __str__(self):
        return self.title


class Document(models.Model):
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('pending', 'Pending'),
    ]

    title = models.ForeignKey(Type, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    file = models.FileField(blank=True, null=True)
    def __str__(self):
        return f'{self.title} - {self.status}'