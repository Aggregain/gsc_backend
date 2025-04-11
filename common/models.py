from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата последнего обновления')

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='название страны', unique=True)
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'


class City(BaseModel):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='страна')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='название города', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'


class EducationPlace(BaseModel):
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='город')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='название учебного заведения', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'учебное заведение'
        verbose_name_plural = 'учебные заведения'
