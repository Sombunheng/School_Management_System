# Generated by Django 4.2.7 on 2024-08-22 06:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0001_initial"),
        ("academics", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="examresult",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exam_results",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="exam",
            name="class_instance",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exams",
                to="academics.classroom",
            ),
        ),
        migrations.AddField(
            model_name="exam",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exams",
                to="academics.course",
            ),
        ),
        migrations.AddField(
            model_name="enrollment",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="enrollments",
                to="academics.course",
            ),
        ),
        migrations.AddField(
            model_name="enrollment",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="enrollments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="school",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="courses",
                to="school.school",
            ),
        ),
        migrations.AddField(
            model_name="classroom",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="classes",
                to="academics.course",
            ),
        ),
        migrations.AddField(
            model_name="classroom",
            name="teacher",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="classes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="class_instance",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attendances",
                to="academics.classroom",
            ),
        ),
        migrations.AddField(
            model_name="attendance",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attendances",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="enrollment",
            unique_together={("student", "course")},
        ),
        migrations.AlterUniqueTogether(
            name="attendance",
            unique_together={("student", "class_instance", "date")},
        ),
    ]