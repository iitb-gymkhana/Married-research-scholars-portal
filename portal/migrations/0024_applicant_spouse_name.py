# Generated by Django 3.0.7 on 2020-09-24 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0023_auto_20200922_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='spouse_name',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
