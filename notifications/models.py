from common.models import BaseModel
from django.db import models
from applications.constants import StatusChoices

class Notification(BaseModel):
    receiver = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, verbose_name='получатель',
                                 related_name='notifications')
    type = models.CharField(max_length=255, verbose_name='тип', choices=StatusChoices,)
    content = models.TextField(verbose_name='контент')
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE,verbose_name='заявка',
                                    related_name='notifications')
    is_seen = models.BooleanField(default=False, verbose_name='прочитано')

    class Meta:
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'

    def __str__(self):
        return f'{self.content}'