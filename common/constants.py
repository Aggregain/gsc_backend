from django.db import models


class DegreeChoices(models.TextChoices):
    bachelor = 'BACHELOR', 'bachelor'
    masters = 'MASTERS', 'masters'
    mba = 'MBA', 'mba'
    phd = 'PHD', 'phd'


class FormatChoices(models.TextChoices):
    online = 'ONLINE', 'online'
    offline = 'OFFLINE', 'offline'


class LanguageChoices(models.TextChoices):
    english = 'ENGLISH', 'english'
    french = 'FRENCH', 'french'
    spanish = 'SPANISH', 'spanish'
    russian = 'RUSSIAN', 'russian'


