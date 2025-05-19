from common.models import BaseModel
from django.db import models
from applications.constants import StatusChoices

class Notification(BaseModel):
    receiver = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, verbose_name='получатель',
                                 related_name='notifications', db_index=True)
    type = models.CharField(max_length=255, verbose_name='тип', choices=StatusChoices, db_index=True)
    content = models.TextField(verbose_name='контент', null=True, blank=True)
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE,verbose_name='заявка',
                                    related_name='notifications', db_index=True)
    is_seen = models.BooleanField(default=False, verbose_name='прочитано', db_index=True)

    class Meta:
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'

    def __str__(self):
        return f'{self.content}'