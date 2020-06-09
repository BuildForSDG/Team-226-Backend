# Generated by Django 3.0.6 on 2020-05-30 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("resources", "0017_auto_20200530_0901"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commentimage",
            name="upload_for",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comment_images",
                to="resources.Comment",
                verbose_name="Comment Linked to",
            ),
        ),
    ]
