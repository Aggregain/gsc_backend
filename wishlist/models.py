from django.db import models
from django.contrib.auth import get_user_model

from common.models import Program

User = get_user_model()

class WishlistItem(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='аккаунт',
                                related_name='wishlist')
    program = models.ForeignKey(Program, on_delete=models.CASCADE,verbose_name='программа',
                                related_name='wishlists')

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'элемент избранного'
        unique_together = ('account', 'program')
