from django.db import models

from common.models import BaseModel, EducationPlace, Program
from . import constants

def application_files_upload_to(instance, filename):
    return f'applications/{instance.name}/{filename}'

class Application(BaseModel):
    name = models.CharField(max_length=255, verbose_name='название', null=True, blank=True, db_index=True)

    owner = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, verbose_name='владелец', related_name='owned_applications')
    assignee = models.ForeignKey('accounts.Account', on_delete=models.PROTECT, verbose_name='менеджер', related_name='assigned_applications')
    program = models.ForeignKey(Program, on_delete=models.PROTECT, verbose_name='программа', related_name='applications')

    comment = models.TextField(null=True, blank=True, verbose_name='комментарий')
    comment_file = models.FileField(verbose_name='закрепленный файл комментария',
                                    upload_to=application_files_upload_to, null=True, blank=True)

    offer = models.FileField(verbose_name='оффер', upload_to=application_files_upload_to, null=True, blank=True)
    status = models.CharField(max_length=255, choices=constants.StatusChoices, verbose_name='статус', db_index=True)


    def __str__(self):
        return f'{self.name} {self.owner}'



    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'




