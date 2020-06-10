# Generated by Django 3.0.6 on 2020-05-20 14:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("resources", "0005_auto_20200520_1204"),
    ]

    operations = [
        migrations.RemoveField(model_name="landimage", name="uploaded_for",),
        migrations.AddField(
            model_name="landimage",
            name="upload_for",
            field=models.ForeignKey(
                db_column="upload_for",
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="land_images",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Land Linked to",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="land",
            name="title",
            field=models.CharField(
                max_length=255, unique=True, verbose_name="Land title"
            ),
        ),
    ]
