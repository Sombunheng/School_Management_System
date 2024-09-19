from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    established_date = models.DateField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name


class Branch(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='branches' )
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=255)
    user_id = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='branches' ,default=1)

    
    def __str__(self):
        return f'{self.name} - {self.school.name}'


