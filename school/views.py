from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import School, Branch
from .serializers import SchoolSerializer, BranchSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    authentication_classes = []  
    queryset = School.objects.all()

    serializer_class = SchoolSerializer
    # permission_classes = [IsAuthenticated]  # Apply authentication permissions

class BranchViewSet(viewsets.ModelViewSet):
    authentication_classes = []  
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    # permission_classes = [IsAuthenticated]  # Apply authentication permissions

    def perform_create(self, serializer):
        # Automatically assign the current user to the `user_id` field
        serializer.save(user_id=self.request.user)
