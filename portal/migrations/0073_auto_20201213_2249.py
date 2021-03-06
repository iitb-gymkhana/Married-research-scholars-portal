# Generated by Django 3.0.7 on 2020-12-13 17:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0072_auto_20201213_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='acad_details_verification_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Verification Date by Academic Section'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='acad_details_verified',
            field=models.BooleanField(default=False, null=True, verbose_name='The academic details are verified and found correct'),
        ),
    ]
