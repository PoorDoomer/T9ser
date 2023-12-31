# Generated by Django 4.2.7 on 2023-11-21 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("t9ser_api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="match",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("ongoing", "Ongoing"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
    ]
