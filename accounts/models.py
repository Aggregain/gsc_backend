from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from accounts.managers import AccountManager
from common.models import BaseModel, EducationPlace, City, Country


def avatar_path(instance, filename):
    return f'avatars/{instance.email}/{filename}'


def attachment_path(instance, filename):
    return f'attachments/{instance.account.email}/{filename}'


class Account(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=255, verbose_name='имя', blank=True, null=True)
    second_name = models.CharField(max_length=255, verbose_name='фамилия', blank=True, null=True)
    last_name = models.CharField(max_length=255, verbose_name='отчество', blank=True, null=True)
    phone_number = models.CharField(max_length=255, verbose_name='номер телефона', null=True, blank=True)
    birth_date = models.DateField(verbose_name='дата рождения', null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True, verbose_name='аватар')

    is_staff = models.BooleanField(default=False, verbose_name='статус админа')
    is_active = models.BooleanField(default=True, verbose_name='статус активности')
    is_superuser = models.BooleanField(default=False, verbose_name='статус суперпользователя')

    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=True, verbose_name='город')
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.PROTECT, verbose_name='страна')
    education_place = models.ForeignKey(EducationPlace, null=True, blank=True, on_delete=models.PROTECT,
                                        verbose_name='учебное заведение')

    objects = AccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'аккаунт'
        verbose_name_plural = 'аккаунты'



class Attachment(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='аккаунт',
                                related_name='attachments')
    name = models.CharField(max_length=255, verbose_name='название файла/сертификата', unique=True)
    grade = models.DecimalField(verbose_name='оценка', null=True, blank=True, max_digits=5, decimal_places=2)
    file = models.FileField(upload_to=attachment_path, null=True, blank=True, verbose_name='файл')
    meta = models.JSONField(null=True, blank=True, verbose_name='дополнительно')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'документ'
        verbose_name_plural = 'документы'

        unique_together = ('account', 'name',)
