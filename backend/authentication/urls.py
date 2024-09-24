from authentication import views
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('register' , views.RegisterAPIView.as_view() , name="register"),
    path('login' , views.LoginAPIView.as_view() , name="login"),
    path('user' , views.AuthUserAPIView.as_view() , name="user"),
    path('teacher' , views.TeacherAPIView.as_view() , name="Teacher"),
    path('teacher/<int:id>/' , views.TeacherDetailAPIView.as_view() , name="Teacher"),
    path('roles' , views.RoleAPIView.as_view() , name="roles"),
    path('roles/<int:id>/' , views.RoleDetailAPIView.as_view() , name="roles"),
    path('profiles' , views.ProfileAPIView.as_view() , name="profiles"),
    path('profiles/<int:id>/' , views.ProfileDetailAPIView.as_view() , name="profiles"),
   
] 
