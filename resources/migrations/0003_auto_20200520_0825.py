# Generated by Django 3.0.6 on 2020-05-20 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("resources", "0002_auto_20200511_1120"),
    ]

    operations = [
        migrations.AddField(
            model_name="land",
            name="currency",
            field=models.CharField(
                choices=[("XAF", "XAF")],
                default="XAF",
                max_length=10,
                verbose_name="Currency",
            ),
        ),
        migrations.AddField(
            model_name="land",
            name="lease_rate_periodicity",
            field=models.CharField(
                choices=[
                    ("h", "hourly"),
                    ("d", "daily"),
                    ("w", "weekly"),
                    ("m", "monthly"),
                    ("y", "yearly"),
                ],
                max_length=10,
                blank=True,
                verbose_name="Lease Rate Periodicity",
            ),
        ),
        migrations.CreateModel(
            name="LandImage",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="land_image_uploads/",
                        verbose_name="Profile picture",
                    ),
                ),
                (
                    "uploaded_for",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Land Linked to",
                    ),
                ),
            ],
        ),
    ]