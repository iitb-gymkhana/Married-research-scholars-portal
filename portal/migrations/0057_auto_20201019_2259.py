# Generated by Django 3.0.7 on 2020-10-19 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0056_auto_20201019_2257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='coursework_grade_sheet',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='coursework_grade_sheet_verified',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='date_of_marriage',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='joint_photograph_with_spouse',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='joint_photograph_with_spouse_verified',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='marriage_certificate',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='marriage_certificate_verified',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='recommendation_of_guide_for_accomodation',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='recommendation_of_guide_for_accomodation_verified',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='spouse_designation',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='spouse_name',
        ),
        migrations.RemoveField(
            model_name='applicant',
            name='spouse_roll_number',
        ),
    ]
