# Generated by Django 5.1.1 on 2024-10-17 08:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0010_remove_student_classroom_student_classrooms'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='end_time',
            field=models.TimeField(default=datetime.time(17, 0)),
        ),
        migrations.AddField(
            model_name='classroom',
            name='start_time',
            field=models.TimeField(default=datetime.time(9, 0)),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='end_date',
            field=models.DateField(default=datetime.date(2024, 12, 31)),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='start_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]