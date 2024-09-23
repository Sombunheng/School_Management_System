from rest_framework import serializers
from authentication.models import User ,UserRole ,Teacher , Profile
from school.models import School

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        max_length=128 , min_length=6 , write_only=True
    )
    
    class Meta:
        model = User
        fields = ('username' , 'email'  , 'password')
        
    def create(self, validated_data):
        # Automatically assign a fixed role during creation
        user = User.objects.create_user(**validated_data)
        fixed_role_id = 1  # Set a default role (e.g., ID of 'Teacher' role)
        user.roles_id = fixed_role_id
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128 , min_length=6 , write_only=True
    )
    
    class Meta:
        model = User
        fields = ('username' , 'email' , 'password' , 'token')
        
        read_only_fields = ['token']
        
class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'name', 'description']

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(queryset=UserRole.objects.all())
    # roles = UserRoleSerializer( read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'email_verified', 'roles']
    
    # def create(self, validated_data):
    #     roles = validated_data.pop('roles')
    #     user = User.objects.create(**validated_data)
    #     if roles: 
    #         user.roles.set(roles)
    #     return user

    # def update(self, instance, validated_data):
    #     roles = validated_data.pop('roles')
    #     instance = super().update(instance, validated_data)
    #     if roles is not None:
    #         instance.roles.set(roles)
    #     return instance     
    
class TeacherSerializer(serializers.ModelSerializer):
    user = RegisterSerializer()  # Nested UserSerializer

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'school', 'specialization', 'hire_date']
        read_only_fields = ['id']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        roles = UserRole.objects.get(id=3)
        fixed_role_id = roles
        user.roles = fixed_role_id
        user.save()

        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.school = validated_data.get('school', instance.school)
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.hire_date = validated_data.get('hire_date', instance.hire_date)

        instance.save()
        roles = UserRole.objects.get(id=3)

        fixed_role_id = roles
        user.roles = fixed_role_id
        user.save()

        return instance
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user' , 'profile_image' ]

