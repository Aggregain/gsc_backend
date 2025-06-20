# Generated by Django 5.1.7 on 2025-05-15 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0008_application_comment_file_application_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='name',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('DRAFT', 'черновик'), ('IN_PROGRESS', 'в работе'), ('DENIED', 'отказано'), ('ACCEPTED', 'принято'), ('FOR_REVISION', 'на доработку'), ('FOR_CONSIDERATION', 'на рассмотрении')], db_index=True, max_length=255, verbose_name='статус'),
        ),
    ]
