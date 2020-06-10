# Generated by Django 3.0.6 on 2020-05-21 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0010_auto_20200521_0654"),
    ]

    operations = [
        migrations.RenameField(
            model_name="list", old_name="user", new_name="created_by",
        ),
        migrations.RemoveField(model_name="list", name="posts",),
        migrations.AlterField(
            model_name="list",
            name="cover_image",
            field=models.ImageField(
                blank=True, upload_to="", verbose_name="Cover image"
            ),
        ),
        migrations.CreateModel(
            name="ListPost",
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
                    "list",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="resources.List"
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="resources.Post"
                    ),
                ),
            ],
        ),
    ]
