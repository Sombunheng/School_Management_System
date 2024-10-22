from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import School, Branch
from .serializers import SchoolSerializer, BranchSerializer
from authentication.permission import IsSuperUser , AdminOrReanOnly , TeacherOrReadOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from authentication.pagination import CustomPageNumberPagination


class SchoolViewSet(ListCreateAPIView):
    permission_classes = [ IsSuperUser  ]
    pagination_class = CustomPageNumberPagination
    serializer_class = SchoolSerializer

    
    def perform_create(self , serializer):
        return serializer.save()
    
    def get_queryset(self):        
        return School.objects.all()
 
class SchoolDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [ IsSuperUser ]

    serializer_class = SchoolSerializer
    lookup_field = "id"
    
    def get_queryset(self):
        return School.objects.all()
    

class BranchViewSet(viewsets.ModelViewSet):
    # authentication_classes = []  
    permission_classes = [ IsSuperUser]
    pagination_class = CustomPageNumberPagination

    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    # permission_classes = [IsAuthenticated]  # Apply authentication permissions

    def perform_create(self, serializer):
        # Automatically assign the current user to the `user_id` field
        serializer.save(user_id=self.request.user)
