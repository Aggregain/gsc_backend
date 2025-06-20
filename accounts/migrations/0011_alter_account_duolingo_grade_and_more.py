# Generated by Django 5.1.7 on 2025-06-08 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_attachment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='duolingo_grade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='оценка DUOLINGO'),
        ),
        migrations.AlterField(
            model_name='account',
            name='gmat_grade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='оценка GMAT'),
        ),
        migrations.AlterField(
            model_name='account',
            name='gpa_grade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='оценка GPA'),
        ),
        migrations.AlterField(
            model_name='account',
            name='gre_grade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='оценка GRE'),
        ),
        migrations.AlterField(
            model_name='account',
            name='ielts_grade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='оценка IELTS'),
        ),
        migrations.AlterField(
            model_name='account',
            name='sat_grade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='оценка SAT'),
        ),
        migrations.AlterField(
            model_name='account',
            name='toefl_grade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='оценка TOEFL'),
        ),
    ]
