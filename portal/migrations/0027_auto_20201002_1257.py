# Generated by Django 3.1.1 on 2020-10-02 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0026_auto_20201002_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='date_of_marriage',
            field=models.DateField(default='', null=True),
        ),
    ]