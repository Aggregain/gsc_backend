from django.db import models
from ckeditor.fields import RichTextField
from . import constants


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
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='страна', related_name='cities')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='название города', unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'


class EducationPlace(BaseModel):
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='город', related_name='education_places')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='название учебного заведения',
                            unique=True)
    description = RichTextField(null=True, blank=True, verbose_name='описание')
    is_for_admission = models.BooleanField(default=True, verbose_name='доступно для поступления')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'учебное заведение'
        verbose_name_plural = 'учебные заведения'


class Specialty(BaseModel):
    name = models.CharField(max_length=255, verbose_name='название специальности')
    education_place = models.ForeignKey(EducationPlace, on_delete=models.PROTECT, verbose_name='универ', related_name='specialities')
    description = RichTextField(verbose_name='описание', null=True, blank=True)
    degree = models.CharField(max_length=128, verbose_name='степень', choices=constants.DegreeChoices)

    def __str__(self):
        return f'{self.name} {self.education_place}'

    class Meta:
        verbose_name = 'специальность'
        verbose_name_plural = 'специальности'
        unique_together = ('education_place', 'degree', 'name')
