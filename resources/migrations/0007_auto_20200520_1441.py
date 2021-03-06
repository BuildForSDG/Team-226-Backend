# Generated by Django 3.0.6 on 2020-05-20 14:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("resources", "0006_auto_20200520_1439"),
    ]

    operations = [
        migrations.AlterField(
            model_name="landimage",
            name="upload_for",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="land_images",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Land Linked to",
            ),
        ),
    ]
