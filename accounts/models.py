from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from applications.models import Application
from accounts.managers import AccountManager
from common.models import BaseModel, EducationPlace, City, Country
from common.constants import DegreeChoices

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
    is_active = models.BooleanField(default=False, verbose_name='статус активности')
    is_superuser = models.BooleanField(default=False, verbose_name='статус суперпользователя')

    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=True, verbose_name='город', db_index=True, related_name='accounts')
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.PROTECT, verbose_name='страна', db_index=True, related_name='accounts')
    education_place = models.ForeignKey(EducationPlace, null=True, blank=True, on_delete=models.PROTECT,
                                        verbose_name='учебное заведение', db_index=True, related_name='accounts')

    ielts_grade = models.DecimalField(verbose_name='оценка IELTS', null=True, blank=True, max_digits=10, decimal_places=2)
    toefl_grade =  models.DecimalField(verbose_name='оценка TOEFL', null=True, blank=True, max_digits=10, decimal_places=2)
    sat_grade =  models.DecimalField(verbose_name='оценка SAT', null=True, blank=True, max_digits=10, decimal_places=2)
    duolingo_grade =  models.DecimalField(verbose_name='оценка DUOLINGO', null=True, blank=True, max_digits=10, decimal_places=2)
    gpa_grade =  models.DecimalField(verbose_name='оценка GPA', null=True, blank=True, max_digits=10, decimal_places=2)
    gmat_grade =  models.DecimalField(verbose_name='оценка GMAT', null=True, blank=True, max_digits=10, decimal_places=2)
    gre_grade =  models.DecimalField(verbose_name='оценка GRE', null=True, blank=True, max_digits=10, decimal_places=2)

    degree = models.CharField(verbose_name='академическая степень', choices=DegreeChoices, null=True, blank=True, max_length=128)

    objects = AccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'аккаунт'
        verbose_name_plural = 'аккаунты'

    @property
    def email_confirmation_url(self):
        token = default_token_generator.make_token(self)
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        confirmation_url = f"{settings.BACKEND_BASE_URL}/api/accounts/email/confirm/{uid}/{token}"
        return confirmation_url

    @property
    def password_reset_url(self):
        token = default_token_generator.make_token(self)
        uid = urlsafe_base64_encode(force_bytes(self.pk))
        reset_url = f"{settings.FRONTEND_BASE_URL}/reset-password/{uid}/{token}"
        return reset_url



class Attachment(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='аккаунт',
                                related_name='attachments', db_index=True)
    name = models.CharField(max_length=255, verbose_name='название файла/сертификата',)
    file = models.FileField(upload_to=attachment_path, null=True, blank=True, verbose_name='файл')
    meta = models.CharField(null=True, blank=True, verbose_name='дополнительно', max_length=255)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name='заявка', related_name='attachments')
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'документ'
        verbose_name_plural = 'документы'


