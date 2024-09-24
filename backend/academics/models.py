from django.utils import timezone
from django.db import models

# Create your models here.

class Program(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, related_name='program' , default=1)
    def __str__(self):
        return f'program name :{self.name} '

class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    credits = models.PositiveIntegerField()
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey('school.School', on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f'{self.name} ({self.code})'
    
class Classroom(models.Model):
    name = models.CharField(max_length=255)
    courses = models.ManyToManyField(Course , related_name='courses_classroom')
    teacher = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, related_name='classes')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.name} - {self.courses.name}'

class Attendance(models.Model):
    student = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='attendances')
    class_instance = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')], default='absent')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'class_instance', 'date')
        
    def __str__(self):
        return f'{self.student.username} - {self.class_instance.name} - {self.date}'
    
class Exam(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    class_instance = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='exams', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    exam_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.title} - {self.course.name} - {self.exam_date}'
    
class ExamResult(models.Model):
    student = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='exam_results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=10, blank=True, null=True)  # Optional field for grade representation

    def __str__(self):
        return f'{self.student.username} - {self.exam.title} - {self.score}'

class Student(models.Model):
    
    MALE = 'Male'
    FEMALE = 'Female'
    
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    
    first_name = models.CharField(max_length=255, default='')
    last_name = models.CharField(max_length=255, default='')
    age = models.IntegerField(default=1)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default=MALE,
    )
    dob = models.DateField(default=timezone.now, verbose_name='Date of Birth')
    pob = models.CharField(max_length=255, verbose_name='Place of Birth', default='')
    nationality = models.CharField(max_length=225, default='')
    belt_level = models.CharField(max_length=50, verbose_name='Belt Level', default='')
    phone = models.CharField(max_length=255, default='')
    email = models.EmailField(default='')
    mother_name = models.CharField(max_length=255, verbose_name="Mother's Name", default='')
    mother_occupation = models.CharField(max_length=255, verbose_name="Mother's Occupation", default='')
    father_name = models.CharField(max_length=255, verbose_name="Father's Name", default='')
    father_occupation = models.CharField(max_length=255, verbose_name="Father's Occupation", default='')
    address = models.CharField(max_length=255, default='')
    parent_contact = models.CharField(max_length=255, verbose_name="Parent's Contact", default='')
    student_passport = models.CharField(max_length=255, verbose_name='Student Passport', default='')
    admission_date = models.DateField(default=timezone.now)
    courses = models.ManyToManyField(Course, related_name='students')
    branch = models.ForeignKey('school.Branch', on_delete=models.CASCADE, related_name='students')
    image = models.ImageField(upload_to='students/images/', blank=True, null=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
 
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
    phone = models.CharField(max_length=20)  
    number_student = models.IntegerField(default=0)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    programs = models.ManyToManyField(Program , related_name='program')  
    assign_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='user_recieved')
    handle_by = models.ManyToManyField('authentication.User', related_name='user_handle')  

    def __str__(self):
        return f"{self.client} - {self.get_status_display()} - {self.programs} - {self.handle_by}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    courses = models.ManyToManyField(Course , related_name='courses_enrollment')
    enrollment_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.student.username} enrolled in {self.courses.name}'
    