# Generated by Django 3.0.2 on 2020-01-21 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portal", "0006_auto_20200121_1901"),
    ]

    operations = [
        migrations.AlterField(
            model_name="queuer",
            name="proof_document",
            field=models.FileField(upload_to="marriage_certi/"),
        ),
    ]