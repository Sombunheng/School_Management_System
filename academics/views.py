from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class StudentAPIView(ListCreateAPIView):
    authentication_classes = []  
    serializer_class = StudentSerializer
    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Student.objects.all()
    
class StudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    authentication_classes = []  
    # permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_queryset(self):
        return Student.objects.all()

class TrailAPIView(ListCreateAPIView):
    authentication_classes = []  
    serializer_class = TrailSerializer
    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Trail.objects.all()
 
class TrailDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TrailSerializer
    authentication_classes = []  
    # permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_queryset(self):
        return Trail.objects.all()

class ProgramAPIView(ListCreateAPIView):
    authentication_classes = []  
    serializer_class = ProgramSerializer
    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):        
        return Program.objects.all()
 
class ProgramDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProgramSerializer
    authentication_classes = []  
    # permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_queryset(self):
        return Program.objects.all()
    
class CourseAPIView(ListCreateAPIView):
    authentication_classes = []  
    serializer_class = CourseSerializer
    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Course.objects.all()
 
class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    authentication_classes = []  
    # permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_queryset(self):
        return Course.objects.all()

class ClassroomAPIView(ListCreateAPIView):
    authentication_classes = []  
    serializer_class = ClassroomSerializer
    
    def perform_create(self , serializer):
        # course = get_object_or_404(Course, id=self.request.data.get('course_id'))
        return serializer.save()
    
    def get_queryset(self):
        return Classroom.objects.all()
 
class ClassroomDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    authentication_classes = []  
    # permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_queryset(self):
        return Classroom.objects.all()
    
class EnrollmentAPIView(ListCreateAPIView):
    authentication_classes = []  
    serializer_class = EnrollmentSerializer
    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Enrollment.objects.all()
    
class EnrollmentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EnrollmentSerializer
    authentication_classes = []  
    # permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    
    def get_queryset(self):
        return Enrollment.objects.all()
    
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    # permission_classes = []
    authentication_classes = []  


    def get_queryset(self):
        # Optionally, filter the attendance records for the authenticated user
        user = self.request.user
        return self.queryset.filter(student=user) if user.is_student else self.queryset

    def perform_create(self, serializer):
        serializer.save()
    
