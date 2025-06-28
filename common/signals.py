from django.db.models.signals import post_save
from . import models
from django.dispatch import receiver
from django.db.models import Max, Min

@receiver(post_save, sender=models.Program)
def change_prices_data(sender, instance, **kwargs):
    education_place = instance.education_place
    if education_place.prices_data:
        education_place.prices_data[instance.name] = str(instance.price)
    else:
        education_place.prices_data = {instance.name: str(instance.price)}
    education_place.save()


@receiver(post_save, sender=models.Specialty)
def change_durations(sender, instance, **kwargs):
    program = instance.program
    specialties = program.specialties.all()
    max_duration = specialties.aggregate(Max('duration'))['duration__max']
    min_duration = specialties.aggregate(Min('duration'))['duration__min']
    if program.specialty_durations:
        program.specialty_durations['max_duration'] = max_duration
        program.specialty_durations['min_duration'] = min_duration
    else:
        program.specialty_durations = {'max_duration': max_duration, 'min_duration': min_duration}
    program.save()


