# Generated by Django 3.0.6 on 2020-05-21 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0013_auto_20200521_2306"),
    ]

    operations = [
        migrations.AlterField(
            model_name="land",
            name="lease_rate_periodicity",
            field=models.CharField(
                blank=True,
                choices=[
                    ("h", "hourly"),
                    ("d", "daily"),
                    ("w", "weekly"),
                    ("m", "monthly"),
                    ("y", "yearly"),
                ],
                default="",
                max_length=10,
                verbose_name="Lease Rate Periodicity",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="list",
            name="cover_image",
            field=models.ImageField(
                blank=True, default="", upload_to="", verbose_name="Cover image"
            ),
            preserve_default=False,
        ),
    ]
