# Generated by Django 3.0.7 on 2020-12-13 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0068_auto_20201213_1923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicant',
            old_name='scholar_awarded_upto',
            new_name='scholarship_awarded_upto',
        ),
    ]