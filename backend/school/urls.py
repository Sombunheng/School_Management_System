from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, BranchViewSet

router = DefaultRouter()
router.register(r'schools', SchoolViewSet)
router.register(r'branches', BranchViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
