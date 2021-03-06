# Generated by Django 3.0.7 on 2020-10-16 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0048_remove_applicant_vacate'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='coursework_grade_sheet',
            field=models.FileField(null=True, upload_to='grade_sheet/'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='joint_photograph_with_spouse',
            field=models.FileField(null=True, upload_to='photo_with_spouse/'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='marriage_certificate',
            field=models.FileField(null=True, upload_to='marriage_certificates/'),
        ),
        migrations.AddField(
            model_name='applicant',
            name='recommendation_of_guide_for_accomodation',
            field=models.FileField(null=True, upload_to='guide_recommendation/'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='spouse_name',
            field=models.CharField(default='Spouse', max_length=128, null=True),
        ),
    ]
