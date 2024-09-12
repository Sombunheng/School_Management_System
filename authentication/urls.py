from authentication import views
from django.urls import path

urlpatterns = [
    path('register' , views.RegisterAPIView.as_view() , name="register"),
    path('login' , views.LoginAPIView.as_view() , name="login"),
    path('user' , views.AuthUserAPIView.as_view() , name="user"),
    path('role' , views.RoleAPIView.as_view() , name="Teacher"),
    path('teacher' , views.TeacherAPIView.as_view() , name="Teacher"),
    path('teacher/<int:id>/' , views.TeacherDetailAPIView.as_view() , name="Teacher")
]
