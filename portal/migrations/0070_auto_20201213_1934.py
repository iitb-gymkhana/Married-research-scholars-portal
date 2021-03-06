# Generated by Django 3.0.7 on 2020-12-13 14:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0069_auto_20201213_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='date_applied',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date Applied'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='verified_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Date of verification by HCU'),
        ),
    ]
