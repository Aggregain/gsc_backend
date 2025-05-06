from django.db import models


class StatusChoices(models.TextChoices):
    DRAFT = 'DRAFT', 'черновик'
    IN_PROGRESS = 'IN_PROGRESS', 'в работе'
    DENIED = 'DENIED', 'отказано'
    ACCEPTED = 'ACCEPTED', 'принято'
    FOR_REVISION = 'FOR_REVISION',  'на доработку'
    FOR_CONSIDERATION = 'FOR_CONSIDERATION', 'на рассмотрении'
