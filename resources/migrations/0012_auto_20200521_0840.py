# Generated by Django 3.0.6 on 2020-05-21 08:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("resources", "0011_auto_20200521_0734"),
    ]

    operations = [
        migrations.AddField(
            model_name="listpost",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="listpost", unique_together={("list", "post")},
        ),
    ]
