# Generated by Django 3.0.7 on 2020-12-13 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0073_auto_20201213_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='acad_details_verified',
            field=models.BooleanField(default=False, verbose_name='The academic details are verified and found correct'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='application_received_by_hcu_date',
            field=models.DateTimeField(default='', null=True, verbose_name='Application Received by H.C.Unit Date:'),
        ),
    ]
