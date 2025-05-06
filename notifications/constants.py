from django.db import models

class NotificationTypes(models.TextChoices):
    SUCCESS = "SUCCESS", "успех"
    FAILURE = "FAILURE", "провал"