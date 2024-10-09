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

class TeacherOrReadOnly(BasePermission):
   def has_object_permission(self, request, view):
      if request.method in permissions.SAFE_METHODS:
         return True
      
      if request.user.roles.id == 1:
         return True
      return False

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
      print("is user" , request.user)
      if request.method in permissions.SAFE_METHODS:
         return True
      
      if request.user and request.user.is_authenticated:
         print("is superuser:", request.user.is_superuser)

         # Return True only if the user is a superuser
         if request.user.is_superuser:
            return True

      # Return False if the user is not a superuser or not authenticated
      return False

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_permission(self, request, view):
        print("work or not")
        # Allow any authenticated user to make a POST request (create)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For other methods (GET, PUT, DELETE), check object ownership
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for all authenticated users.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the profile.
        return obj.user == request.user

