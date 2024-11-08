# Generated by Django 4.2.7 on 2024-07-29 07:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_trail_programs"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trail",
            name="handle_by",
        ),
        migrations.AlterField(
            model_name="trail",
            name="programs",
            field=models.ManyToManyField(related_name="program", to="network.program"),
        ),
        migrations.AddField(
            model_name="trail",
            name="handle_by",
            field=models.ManyToManyField(
                related_name="user_handle", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
