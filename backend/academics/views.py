from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from authentication.permission import AdminOrReanOnly , TeacherOrReadOnly



class StudentAPIView(ListCreateAPIView):
    # authentication_classes = []  
    permission_classes = [AdminOrReanOnly]
    serializer_class = StudentSerializer
    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Student.objects.all()
    
class StudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializer
    # authentication_classes = []  

    permission_classes = [AdminOrReanOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Student.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        # Get the course object to be deleted
        instance = self.get_object()
        instance.delete()  # Delete the instance

        # Return a custom response with a success message
        return Response({"message": "Student deleted successfully!"}, status=status.HTTP_200_OK)

class TrailAPIView(ListCreateAPIView):
    # authentication_classes = []  
    serializer_class = TrailSerializer
    permission_classes = [AdminOrReanOnly]

    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Trail.objects.all()
 
class TrailDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TrailSerializer
    permission_classes = [AdminOrReanOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Trail.objects.all()

class ProgramAPIView(ListCreateAPIView):
    serializer_class = ProgramSerializer
    permission_classes = [AdminOrReanOnly]

    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):        
        return Program.objects.all()
 
class ProgramDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProgramSerializer
    permission_classes = [AdminOrReanOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Program.objects.all()
    
class CourseAPIView(ListCreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AdminOrReanOnly]

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Course.objects.all()
 
class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AdminOrReanOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Course.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        # Get the course object to be deleted
        instance = self.get_object()
        instance.delete()  # Delete the instance

        # Return a custom response with a success message
        return Response({"message": "Course deleted successfully!"}, status=status.HTTP_200_OK)

class ClassroomAPIView(ListCreateAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [AdminOrReanOnly , TeacherOrReadOnly]

    def perform_create(self , serializer):
        # course = get_object_or_404(Course, id=self.request.data.get('course_id'))
        return serializer.save()
    
    def get_queryset(self):
        return Classroom.objects.all()
 
class ClassroomDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    permission_classes = [AdminOrReanOnly , TeacherOrReadOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Classroom.objects.all()
    
class EnrollmentAPIView(ListCreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [AdminOrReanOnly , TeacherOrReadOnly]

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Enrollment.objects.all()
    
class EnrollmentDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [AdminOrReanOnly | TeacherOrReadOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Enrollment.objects.all()
    
class AttendanceViewSet(viewsets.ModelViewSet):

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [AdminOrReanOnly , TeacherOrReadOnly]

    def perform_create(self, serializer):
        # Customize any creation logic here if needed
        serializer.save()

    def get_queryset(self):
        # Customize the queryset to filter attendance records if needed
        queryset = super().get_queryset()
        # Example: Filter by current user
        # queryset = queryset.filter(student=self.request.user)
        return queryset

class ExamViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminOrReanOnly , TeacherOrReadOnly]
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def perform_create(self, serializer ):
         # Customize any creation logic here if needed
        serializer.save()

    def get_queryset(self):
        authentication_classes = []  
        # Customize the queryset to filter attendance records if needed
        queryset = super().get_queryset()
        # Example: Filter by current user
        # queryset = queryset.filter(student=self.request.user)
        return queryset

class ExamResultViewSet(viewsets.ModelViewSet):

    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer
    permission_classes = [AdminOrReanOnly , TeacherOrReadOnly]

    def perform_create(self, serializer):
        # Customize any creation logic here if needed
        serializer.save()

    def get_queryset(self):
        # Customize the queryset to filter attendance records if needed
        queryset = super().get_queryset()
        # Example: Filter by current user
        # queryset = queryset.filter(student=self.request.user)
        return queryset