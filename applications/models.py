from django.db import models

from common.models import BaseModel, EducationPlace, Program
from . import constants


class Application(BaseModel):
    name = models.CharField(max_length=255, verbose_name='название', null=True, blank=True)

    owner = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, verbose_name='владелец', related_name='owned_applications')
    assignee = models.ForeignKey('accounts.Account', on_delete=models.PROTECT, verbose_name='менеджер', related_name='assigned_applications')
    program = models.ForeignKey(Program, on_delete=models.PROTECT, verbose_name='программа', related_name='applications')


    status = models.CharField(max_length=255, choices=constants.StatusChoices, verbose_name='статус')

    def __str__(self):
        return f'{self.name} {self.owner}'



    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'


