# Generated by Django 5.1.7 on 2025-05-12 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0006_alter_comment_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='комментарий'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
