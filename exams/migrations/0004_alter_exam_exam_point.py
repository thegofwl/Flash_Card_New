# Generated by Django 4.2.4 on 2023-08-24 04:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("exams", "0003_exam_exam_difficulty"),
    ]

    operations = [
        migrations.AlterField(
            model_name="exam",
            name="exam_point",
            field=models.FloatField(),
        ),
    ]
