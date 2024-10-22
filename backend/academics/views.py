from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from authentication.permission import AdminOrReanOnly , TeacherOrReadOnly , IsSuperUser
from rest_framework.views import APIView
from .pagination import CustomPageNumberPagination


class StudentAPIView(ListCreateAPIView):

    permission_classes = [ IsSuperUser | AdminOrReanOnly | TeacherOrReadOnly]

    serializer_class = StudentSerializer
    
    pagination_class = CustomPageNumberPagination

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Student.objects.all()
    
class StudentDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsSuperUser | AdminOrReanOnly | TeacherOrReadOnly]

    serializer_class = StudentSerializer

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
    permission_classes = [ IsSuperUser | AdminOrReanOnly ]
    serializer_class = TrailSerializer

    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Trail.objects.all()
 
class TrailDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsSuperUser | AdminOrReanOnly ]

    serializer_class = TrailSerializer
    permission_classes = [AdminOrReanOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Trail.objects.all()

class ProgramAPIView(ListCreateAPIView):
    permission_classes = [ IsSuperUser | AdminOrReanOnly ]

    serializer_class = ProgramSerializer
    pagination_class = CustomPageNumberPagination
    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):        
        return Program.objects.all()
 
class ProgramDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsSuperUser | AdminOrReanOnly]

    serializer_class = ProgramSerializer
    permission_classes = [AdminOrReanOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Program.objects.all()
    
class CourseAPIView(ListCreateAPIView):
    permission_classes = [ IsSuperUser | AdminOrReanOnly ]

    serializer_class = CourseSerializer

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Course.objects.all()
 
class CourseDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsSuperUser | AdminOrReanOnly ]

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
    permission_classes = [IsSuperUser | AdminOrReanOnly ]
    serializer_class = ClassroomSerializer
    pagination_class = CustomPageNumberPagination
    def perform_create(self , serializer):
        # course = get_object_or_404(Course, id=self.request.data.get('course_id'))
        return serializer.save()
    
    def get_queryset(self):
        return Classroom.objects.all()
 
class ClassroomDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsSuperUser | AdminOrReanOnly ]

    serializer_class = ClassroomSerializer
    lookup_field = "id"
    
    def get_queryset(self):
        return Classroom.objects.all()
    
class EnrollmentAPIView(ListCreateAPIView):
    permission_classes = [ IsSuperUser | AdminOrReanOnly ]

    serializer_class = EnrollmentSerializer
    permission_classes = [AdminOrReanOnly , TeacherOrReadOnly]

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Enrollment.objects.all()
    
class EnrollmentDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsSuperUser | AdminOrReanOnly ]

    serializer_class = EnrollmentSerializer
    permission_classes = [AdminOrReanOnly | TeacherOrReadOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Enrollment.objects.all()
    
class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [ IsSuperUser | AdminOrReanOnly | TeacherOrReadOnly]

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

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
    permission_classes = [AdminOrReanOnly | TeacherOrReadOnly]
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
    permission_classes = [ IsSuperUser | AdminOrReanOnly | TeacherOrReadOnly]

    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer

    def perform_create(self, serializer):
        # Customize any creation logic here if needed
        serializer.save()

    def get_queryset(self):
        # Customize the queryset to filter attendance records if needed
        queryset = super().get_queryset()
        # Example: Filter by current user
        # queryset = queryset.filter(student=self.request.user)
        return queryset
    
class AddStudentsToClassroomView(APIView):
    permission_classes = [ IsSuperUser | AdminOrReanOnly | TeacherOrReadOnly]

    def get(self, request, classroom_id):
        # Attempt to retrieve the classroom by ID
        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            return Response({"error": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the list of students in the classroom
        students = classroom.students.all()  # Get all students associated with the classroom
        print("\n whats student" , students)
        serializer = StudentSerializer(students, many=True)  # Use your StudentSerializer here
        print("\n whats student" , serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, classroom_id):
        # Fetch the classroom instance by its ID
        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            return Response({"error": "Classroom not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Use the serializer to process the data
        serializer = AddStudentsToClassroomSerializer(classroom, data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will invoke the update method in the serializer
            return Response({"message": "Students successfully added to the classroom."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)