from authentication import views
from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet

router = DefaultRouter()
router.register(r'roles', RoleViewSet),


urlpatterns = [
    path('register' , views.RegisterAPIView.as_view() , name="register"),
    path('login' , views.LoginAPIView.as_view() , name="login"),
    path('user' , views.AuthUserAPIView.as_view() , name="user"),
    path('teacher' , views.TeacherAPIView.as_view() , name="Teacher"),
    path('teacher/<int:id>/' , views.TeacherDetailAPIView.as_view() , name="Teacher"),
    path('', include(router.urls)),
    path('<int:id>', include(router.urls)),
]
