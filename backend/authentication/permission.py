from rest_framework import permissions 
from rest_framework.permissions import BasePermission

class AdminOrReanOnly(permissions.IsAdminUser):
   def has_permission(self, request, view):
      
      # Allow safe methods for everyone
      print("user" , request.user)
      if request.method in permissions.SAFE_METHODS:
         return True
      
      # Allow access if the user is anonymous
      # if request.user is None or not request.user.is_authenticated:
      #    return True
      
      # Check if the user is authenticated and has the correct role
      if request.user.is_authenticated:
         # Ensure `roles` attribute and its `id` exist
         return hasattr(request.user, 'roles') and request.user.roles.id == 1
      
      return False
   
class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        # Check if the user is authenticated
      if request.user and request.user.is_authenticated:
         print("is superuser:", request.user.is_superuser)

         # Return True only if the user is a superuser
         if request.user.is_superuser:
            return True

      # Return False if the user is not a superuser or not authenticated
      return False

