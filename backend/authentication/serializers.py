from rest_framework import serializers
from authentication.models import User ,UserRole  , Profile
from school.models import Branch
from django.core.exceptions import ValidationError
from school.serializers import BranchSerializer


class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length=128 , min_length=6 , write_only=True
    )
    
    roles = serializers.SlugRelatedField(
        slug_field='id',
        queryset=UserRole.objects.all(),  # Fetches the role by 'id'
        required=False
    )
    branch = serializers.SlugRelatedField(
        slug_field='id',  # Fetches the branch by 'id'
        queryset=Branch.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email','roles', 'password', 'branch', 'specialization', 'hire_date')
        
    def create(self, validated_data):
        # Automatically assign a fixed role during creation
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128 , min_length=6 , write_only=True
    )
    
    class Meta:
        model = User
        fields = ('id' , 'username' , 'email' , 'password' , 'token')
        
        read_only_fields = ['token']
        
class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'name', 'description']

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        slug_field='id',
        queryset=UserRole.objects.all(),  # Assumes UserRole has a 'name' field
        required=False
    )
    branch = serializers.SlugRelatedField(
        slug_field='id',  # Assuming School has a 'name' field
        queryset=Branch.objects.all(),
        required=False
    )

    roles_name = serializers.SerializerMethodField()
    
    branch_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_staff', 'is_active', 'date_joined','roles','roles_name','branch','branch_name',
             'email_verified',  'specialization', 'hire_date', 'token'
        ]
        read_only_fields = ['id', 'date_joined', 'token']

    def get_roles_name(self, obj):
        return obj.roles.name if obj.roles else None    
    
    def get_branch_name(self, obj):
    # Return the name of the branch associated with the user
        return obj.branch.name if obj.branch else None

    def update(self, instance, validated_data):
        # Custom update logic if needed
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
     
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id' ,'user' , 'profile_image' ]

    def validate_profile_image(self, value):
        # Check file size
        max_size = 5 * 1024 * 1024  # 5 MB
        if value.size > max_size:
            raise ValidationError(f"Image size should be less than {max_size / (1024 * 1024)} MB")
        
        # Check file format
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise ValidationError("Only '.png', '.jpg', and '.jpeg' formats are allowed.")
        
        return value