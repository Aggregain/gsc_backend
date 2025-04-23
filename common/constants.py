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


LANGUAGE_TR = [
    {'id': LanguageChoices.english,
     'name': 'Английский'},
    {'id': LanguageChoices.french,
     'name': 'Французкий'},
    {'id': LanguageChoices.spanish,
     'name': 'Испанский'},
    {'id': LanguageChoices.russian,
     'name': 'Русский'},
]

FORMAT_TR = [
    {'id': FormatChoices.online,
     'name': 'Онлайн'},
    {'id': FormatChoices.offline,
     'name': 'Оффлайн'},
]

DEGREE_TR = [
    {'id': DegreeChoices.bachelor,
     'name': 'Бакалавриат'},
    {'id': DegreeChoices.masters,
     'name': 'Магистратура'},
    {'id': DegreeChoices.mba,
     'name': 'МБА'},
    {'id': DegreeChoices.phd,
     'name': 'Докторантура'},
]

CERTS = [
    {'id': 'IELTS', 'name': 'IELTS'},
    {'id': 'TOEFL', 'name': 'TOEFL'},
    {'id': 'DUOLINGO', 'name': 'DUOLINGO'},
    {'id': 'GRE', 'name': 'GRE'},
    {'id': 'GPA', 'name': 'GPA'},
    {'id': 'GMAT', 'name': 'GMAT'},
    {'id': 'SAT', 'name': 'SAT'},
]
