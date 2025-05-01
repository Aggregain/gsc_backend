from django.db import models


class StatusChoices(models.TextChoices):
    draft = 'DRAFT', 'черновик'
    in_progress = 'IN_PROGRESS', 'в работе'
    denied = 'DENIED', 'отказано'
    accepted = 'ACCEPTED', 'принято'
    for_revision = 'FOR_REVISION',  'на доработку'
    for_consideration = 'FOR_CONSIDERATION', 'на рассмотрении'
