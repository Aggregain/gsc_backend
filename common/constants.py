
from django.db import models

class DegreeChoices(models.TextChoices):
    bachelor = 'BACHELOR', 'bachelor'
    masters = 'MASTERS', 'masters'
    mba = 'MBA', 'mba'
