from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, BranchViewSet , SchoolDetailAPIView

router = DefaultRouter()
router.register(r'branches', BranchViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schools/', SchoolViewSet.as_view(), name='School-create'),   
    path('schools/<int:id>/', SchoolDetailAPIView.as_view(), name='School-create'), 
]
