# Generated by Django 3.1.4 on 2020-12-26 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0090_auto_20201226_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='defer_MRSB',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicant',
            name='defer_Tulsi',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='applicant',
            name='defer_Type1',
            field=models.BooleanField(default=False),
        ),
    ]
