from django.db import models
from django.contrib.auth import get_user_model

from common.models import EducationPlace, Program

User = get_user_model()

class WishlistItem(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='аккаунт',
                                related_name='wishlist')

    education_place = models.ForeignKey(EducationPlace, on_delete=models.CASCADE,verbose_name='ВУЗ',
                                        related_name='wishlists')

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'элемент избранного'
        unique_together = ('account', 'education_place')
