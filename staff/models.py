from django.db import models


class Staff(models.Model):
    user = models.OneToOneField('authentication.User', on_delete=models.CASCADE, related_name='staff_profile')
    position = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True, null=True)
    hire_date = models.DateField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='staff_profiles/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.position}'


class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

