# Generated by Django 4.2.7 on 2024-08-22 08:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="branch",
            name="user_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="branches",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]