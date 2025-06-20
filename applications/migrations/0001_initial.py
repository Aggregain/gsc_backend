# Generated by Django 5.1.7 on 2025-04-30 19:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0005_alter_account_degree'),
        ('common', '0010_alter_specialty_education_place_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата последнего обновления')),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                ('status', models.CharField(choices=[('DRAFT', 'черновик'), ('IN_PROGRESS', 'в работе'), ('DENIED', 'отказано'), ('ACCEPTED', 'принято'), ('FOR_REVISION', 'на доработку'), ('FOR_CONSIDERATION', 'на рассмотрении')], max_length=255, verbose_name='статус')),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assigned_applications', to=settings.AUTH_USER_MODEL, verbose_name='менеджер')),
                ('attachments', models.ManyToManyField(related_name='attachments', to='accounts.attachment', verbose_name='документы')),
                ('education_place', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='applications', to='common.program', verbose_name='программа')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_applications', to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'заявка',
                'verbose_name_plural': 'заявки',
            },
        ),
    ]
