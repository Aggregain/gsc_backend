from common.models import BaseModel
from django.db import models
from .constants import NotificationTypes

class Notification(BaseModel):
    receiver = models.ForeignKey('accounts.Account', on_delete=models.CASCADE, verbose_name='получатель',
                                 related_name='notifications')
    type = models.CharField(max_length=255, verbose_name='тип', choices=NotificationTypes, )
    content = models.TextField(verbose_name='контент')
    application = models.ForeignKey('applications.Application', on_delete=models.CASCADE,verbose_name='заявка',
                                    related_name='notifications')

    class Meta:
        verbose_name = 'уведомление'
        verbose_name_plural = 'уведомления'

    def __str__(self):
        return f'{self.id} {self.type}'