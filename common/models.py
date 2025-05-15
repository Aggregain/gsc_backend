from django.db import models
from ckeditor.fields import RichTextField
from . import constants

def education_place_path(instance, filename):
    return f'education_places/{instance.name}/{filename}'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата последнего обновления')

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='название страны', unique=True, db_index=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'


class City(BaseModel):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='страна', related_name='cities', db_index=True)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='название города', unique=True, db_index=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'


class EducationPlace(BaseModel):
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name='город', related_name='education_places', db_index=True)
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='название учебного заведения',
                            unique=True, db_index=True)
    logo = models.ImageField(null=True, blank=True, verbose_name='лого', upload_to=education_place_path)
    image = models.ImageField(null=True, blank=True, verbose_name='фото ВУЗа', upload_to=education_place_path)
    general_description = RichTextField(null=True, blank=True, verbose_name='основное описание')
    campus_description = RichTextField(null=True, blank=True, verbose_name='описание кампуса')
    scholarship_description = RichTextField(verbose_name='описание стипендии', null=True, blank=True)
    link = models.URLField(null=True, blank=True, verbose_name='ссылка на страницу ВУЗа')
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='рейтинг', db_index=True)
    foundation_date = models.DateField(null=True, blank=True, verbose_name='Дата основания', db_index=True)
    prices_data = models.JSONField(null=True, blank=True, verbose_name='цены')
    is_for_admission = models.BooleanField(default=True, verbose_name='доступно для поступления', db_index=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'учебное заведение'
        verbose_name_plural = 'учебные заведения'


class Program(BaseModel):
    name = models.CharField(max_length=128, choices=constants.DegreeChoices, verbose_name='название программы', db_index=True)
    education_place = models.ForeignKey(EducationPlace, verbose_name='учебное заведение', related_name='degrees',
                                        on_delete=models.PROTECT, db_index=True)
    description_general = RichTextField(verbose_name='описание общее', null=True, blank=True)
    description_academic = RichTextField(verbose_name='описание академ требований', null=True, blank=True)
    description_prices = RichTextField(verbose_name='описание цен', null=True, blank=True)

    duration_years = models.PositiveIntegerField(verbose_name='Длительность обучения(лет)', db_index=True)
    admission_deadline = models.DateField(null=True, blank=True, verbose_name='дедлайн подачи', db_index=True)
    specialty_durations = models.JSONField(null=True, blank=True,
                                           verbose_name='мин макс длительность обучения специальностей')
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                blank=True, verbose_name='стоимость обучения', db_index=True)
    language = models.CharField(max_length=128, choices=constants.LanguageChoices, verbose_name='язык обучения', db_index=True)
    format = models.CharField(max_length=128, choices=constants.FormatChoices, verbose_name='формат обучения', db_index=True)

    def __str__(self):
        return f'{self.name} {self.education_place}'

    class Meta:
        verbose_name = 'программа образования'
        verbose_name_plural = 'программы образования'
        unique_together = ('education_place', 'name')


class SpecialtyGroup(BaseModel):
    name = models.CharField(max_length=255, verbose_name='название', unique=True, db_index=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Группа специальностей'
        verbose_name_plural = 'Группы специальностей'


class Specialty(BaseModel):
    name = models.CharField(max_length=255, verbose_name='название специальности', db_index=True)
    education_place = models.ForeignKey(EducationPlace, on_delete=models.PROTECT,
                                        verbose_name='учебное заведение', related_name='specialties', db_index=True)
    description = RichTextField(verbose_name='описание', null=True, blank=True)

    specialty_group = models.ForeignKey(SpecialtyGroup, on_delete=models.PROTECT, verbose_name='группа',
                                        related_name='specialties')
    admission_deadline = models.DateField(null=True, blank=True, verbose_name='дедлайн подачи')
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True,
                                blank=True, verbose_name='стоимость обучения')
    program = models.ForeignKey(Program, verbose_name='программа', related_name='specialties',
                                on_delete=models.PROTECT)
    duration = models.PositiveIntegerField(verbose_name='длительность(лет)', db_index=True)

    def __str__(self):
        return f'{self.name} {self.education_place}'

    class Meta:
        verbose_name = 'специальность'
        verbose_name_plural = 'специальности'
        unique_together = ('education_place', 'program', 'name')


class Deadline(BaseModel):

    program = models.ForeignKey(Program, verbose_name='программа', related_name='deadlines',
                                        on_delete=models.CASCADE)
    name = models.CharField(max_length=255,
                            verbose_name='название дедлайна', db_index=True)
    due_to = models.DateField(verbose_name='до:')

    def __str__(self):
        return f'{self.name} {self.due_to}'

    class Meta:
        verbose_name = 'дедлайн'
        verbose_name_plural = 'дедлайны'
        unique_together = ('program', 'name')


class Expense(BaseModel):

    program = models.ForeignKey(Program, verbose_name='программа', related_name='expenses',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='тип расходов', db_index=True)
    price_per_year_text = models.CharField(max_length=255, verbose_name='цена')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'расход'
        verbose_name_plural = 'расходы'
        unique_together = ('program', 'name')


class AcademicRequirement(BaseModel):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, verbose_name='программа',
                                related_name='academic_requirements')
    name = models.CharField(max_length=255, verbose_name='название требования',db_index=True,)
    treshold = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='пороговый балл')

    def __str__(self):
        return f'{self.name} {self.treshold}'

    class Meta:
        verbose_name = 'академические требования'
        verbose_name_plural = 'академическое требование'
        unique_together = ('program', 'name')
    
    def save(
        self,
        *args,
        **kwargs
    ):
        self.name = self.name.upper()
        return super().save(*args, **kwargs)