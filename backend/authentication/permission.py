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
        #  test = hasattr(request.user, 'roles') and request.user.roles.id == 'admin'
         print("\n\n whatssss??" ,hasattr(request.user, 'roles') and request.user.roles.name == 'admin' ,"\n\n")
         # Ensure `roles` attribute and its `id` exist
         return hasattr(request.user, 'roles') and request.user.roles.name == 'admin'

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
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For other methods (GET, PUT, DELETE), check object ownership
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the profile.
        return obj == request.user


class OnlySuperUserCanUpdateSelf(BasePermission):
    
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow superusers to proceed to the object level check for updates
        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # Only allow superusers to update their own profile
        if request.method in ['PUT', 'PATCH' , 'DELETE']:
            # Check if the user is superuser and the object belongs to the user
            return request.user.is_superuser and obj == request.user

        # Allow read-only access otherwise
        return request.method in permissions.SAFE_METHODS
