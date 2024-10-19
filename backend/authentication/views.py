from django.shortcuts import render
from authentication.serializers import RegisterSerializer , LoginSerializer , UserSerializer  , UserRoleSerializer , ProfileSerializer
from rest_framework import response , status , permissions
from django.contrib.auth import authenticate
from authentication.models import User  , UserRole , Profile
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView,GenericAPIView
from .pagination import CustomPageNumberPagination
from .permission import AdminOrReanOnly , IsSuperUser , IsOwnerOrReadOnly
from rest_framework import viewsets , generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny



# Create your views here.

class RoleAPIView(ListCreateAPIView):

    permission_classes = [  IsSuperUser]
    
    serializer_class = UserRoleSerializer

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return UserRole.objects.all()

class RoleDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserRoleSerializer
    permission_classes = [  IsSuperUser]
    lookup_field = "id"
    
    def get_queryset(self):
        return UserRole.objects.all()

class AuthUserAPIView(ListCreateAPIView):
    permission_classes = [ IsSuperUser]
    
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):
        return User.objects.all()

class AuthUserDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]
    lookup_field = "id"
    
    def get_queryset(self):
        return User.objects.all()


class RegisterAPIView(GenericAPIView):
    permission_classes = [AdminOrReanOnly | IsSuperUser]


    serializer_class = RegisterSerializer
    
    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data , status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
       
class LoginAPIView(GenericAPIView):
    authentication_classes = []  
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        print(f"Authentication classes: {self.authentication_classes}")
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(username=email, password=password)
        print("\n user" , user , "\n")
        if user:
            serializer = self.serializer_class(user, context={'request': request})
            print("Serialized data:", serializer.data)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message': "Invalid credentials, try again."}, status=status.HTTP_401_UNAUTHORIZED)
    


class ProfileAPIView(ListCreateAPIView):
    
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self , serializer):
        user = self.request.user
        print("user in create" , user)
        print("get data" , serializer.validated_data.get("user"))
        if serializer.validated_data.get('user') != user:
            print("this function work ?")
            return Response({"detail": "You can only create your own profile."}, status=status.HTTP_403_FORBIDDEN)
        return serializer.save()
    
    def get_queryset(self):
        return Profile.objects.all()

class ProfileDetailAPIView(RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsOwnerOrReadOnly]
    serializer_class = ProfileSerializer
    # authentication_classes = []  
    lookup_field = "id"
    
    def get_queryset(self):
        return Profile.objects.all()
