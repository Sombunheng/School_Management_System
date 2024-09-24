from django.shortcuts import render
from authentication.serializers import RegisterSerializer , LoginSerializer , UserSerializer , TeacherSerializer , UserRoleSerializer , ProfileSerializer
from rest_framework import response , status , permissions
from django.contrib.auth import authenticate
from authentication.models import User , Teacher , UserRole , Profile
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,GenericAPIView
from .pagination import CustomPageNumberPagination
from .permission import AdminOrReanOnly , IsSuperUser
from rest_framework import viewsets , generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


# Create your views here.

class RoleAPIView(ListCreateAPIView):
    # authentication_classes = [] 
    # permission_classes = [IsSuperUser]

    permission_classes = [AdminOrReanOnly]
    
    serializer_class = UserRoleSerializer

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return UserRole.objects.all()

class RoleDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserRoleSerializer
    # authentication_classes = []  
    permission_classes = [AdminOrReanOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Teacher.objects.all()

class AuthUserAPIView(ListCreateAPIView):
    authentication_classes = []  
    # permission_classes = (permissions.IsAuthenticated,)
    
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return User.objects.all()

class RegisterAPIView(GenericAPIView):
    permission_classes = [IsSuperUser]

    authentication_classes = []  

    serializer_class = RegisterSerializer
    
    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data , status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
       
class LoginAPIView(GenericAPIView):
    
    authentication_classes = []  
    serializer_class = LoginSerializer
    
    def post(self, request):
        print(f"Authentication classes: {self.authentication_classes}")
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=email, password=password)

        if user:
            serializer = self.serializer_class(user, context={'request': request})
            print("Serialized data:", serializer.data)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': "Invalid credentials, try again."}, status=status.HTTP_401_UNAUTHORIZED)
    
class TeacherAPIView(ListCreateAPIView):
    # authentication_classes = [] 
    # permission_classes = [IsSuperUser]

    permission_classes = [AdminOrReanOnly]
    
    serializer_class = TeacherSerializer

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Teacher.objects.all()

class TeacherDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TeacherSerializer
    # authentication_classes = []  
    permission_classes = [AdminOrReanOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Teacher.objects.all()


class ProfileAPIView(ListCreateAPIView):
    # authentication_classes = [] 
    # permission_classes = [IsSuperUser]

    permission_classes = [AdminOrReanOnly]
    
    serializer_class = ProfileSerializer

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return Profile.objects.all()

class ProfileDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    # authentication_classes = []  
    permission_classes = [AdminOrReanOnly]
    lookup_field = "id"
    
    def get_queryset(self):
        return Profile.objects.all()
