from rest_framework import serializers
from .models import School, Branch

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'address', 'phone_number', 'email', 'established_date', 'website']
    def validate_phone_number(self, value):
        # Check if another school already has the same phone number
        if School.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use by another school.")
        return value
    
    def validate_email(self, value):
        # Check if another school already has the same phone number
        if School.objects.filter(email=value).exists():
            raise serializers.ValidationError("This phone number is already in use by another school.")
        return value
    
    def validate_webiste(self, value):
        # Check if another school already has the same phone number
        if School.objects.filter(website=value).exists():
            raise serializers.ValidationError("This phone number is already in use by another school.")
        return value

class BranchSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)  # Nesting the SchoolSerializer for read-only purposes
    school_id = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), source='school', write_only=True)
    
    class Meta:
        model = Branch
        fields = ['id', 'school', 'school_id', 'name', 'address', 'phone_number', 'email', 'location', 'user_id']

    def validate_phone_number(self, value):
        # Check if another school already has the same phone number
        if Branch.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use by another school.")
        return value

    def create(self, validated_data):
        # Get the school data from validated_data
        school = validated_data.pop('school')
        branch = Branch.objects.create(school=school, **validated_data)
        return branch
