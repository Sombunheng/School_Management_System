from django.db import models

class TimetableEntry(models.Model):
    entry_type = models.CharField(max_length=20, choices=[('class', 'Class'), ('exam', 'Exam'), ('activity', 'Activity')])
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)  # e.g., Classroom, online link
    related_class = models.ForeignKey('academics.Classroom', on_delete=models.CASCADE, related_name='timetable_entries', null=True, blank=True)
    related_exam = models.ForeignKey('academics.Exam', on_delete=models.CASCADE, related_name='timetable_entries', null=True, blank=True)
    related_activity = models.CharField(max_length=255, blank=True, null=True)  # If there are other activities

    def __str__(self):
        return f'{self.title} ({self.entry_type}) - {self.start_time}'
