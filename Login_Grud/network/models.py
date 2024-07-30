from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class Role(models.Model):
    name = models.CharField(max_length=255)


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role", null=True, blank=True)


class Program(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

class Trail(models.Model):
    
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    COMPLETED = 'COMPLETED'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed'),
    ]

    client = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)  # Changed to CharField
    number_student = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10,  # Changed to match the length of the longest status
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    programs = models.ManyToManyField(Program , related_name='program')  # Updated to ManyToManyField
    assign_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_recieved')
    handle_by = models.ManyToManyField(User, related_name='user_handle')  # Updated to ManyToManyField

    def __str__(self):
        return f"{self.client} - {self.get_status_display()} - {self.programs} - {self.handle_by}"
    
   
class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='branches')
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='branch', null=True, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
