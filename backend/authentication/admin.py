from django.contrib import admin
from .models import User , UserRole , Teacher
# Register your models here.
admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(Teacher)