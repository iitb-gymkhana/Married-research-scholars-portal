# Generated by Django 3.1.1 on 2020-10-10 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0034_auto_20201010_1857'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='applicant',
            unique_together={('name', 'roll_number')},
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='building',
        ),
    ]
