from authentication import views
from django.urls import path , include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'attendances', AttendanceViewSet),
router.register(r'exams', ExamViewSet)
router.register(r'exam-results', ExamResultViewSet)



urlpatterns = [
    path('students/', StudentAPIView.as_view(), name='student-create'),   
    path('students/<int:id>/', StudentDetailAPIView.as_view(), name='student-create'),   
    path('student_trail/', TrailAPIView.as_view(), name='student-create'),   
    path('student_trail/<int:id>/', TrailDetailAPIView.as_view(), name='student-create'),   
    path('program/', ProgramAPIView.as_view(), name='student-create'),   
    path('program/<int:id>/', ProgramDetailAPIView.as_view(), name='student-create'),   
    path('course/', CourseAPIView.as_view(), name='student-create'),   
    path('course/<int:id>/', CourseDetailAPIView.as_view(), name='student-create'),   
    path('classroom/', ClassroomAPIView.as_view(), name='student-create'),   
    path('classroom/<int:id>/', ClassroomDetailAPIView.as_view(), name='student-create'),   
    path('enrollment/', EnrollmentAPIView.as_view(), name='student-create'),   
    path('enrollment/<int:id>/', EnrollmentDetailAPIView.as_view(), name='student-create'),   
    path('', include(router.urls)),
    path('<int:id>', include(router.urls)),
 
]
