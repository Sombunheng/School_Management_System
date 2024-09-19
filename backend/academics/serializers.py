from rest_framework import serializers
from academics.models import *
from authentication.models import User
from school.models import School, Branch

class CourseSerializer(serializers.ModelSerializer):
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'description', 'credits', 'program', 'school']
        
class ProgramSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ['id', 'name', 'description', 'school', 'courses']

    def get_courses(self, obj):
        # Assuming courses are associated with the same school as the program
        return CourseSerializer(Course.objects.filter(program=obj), many=True).data  

class ClassroomSerializer(serializers.ModelSerializer):
    
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all() ,many=True )
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles=3))
    course_name = serializers.SerializerMethodField()
    teacher_name = serializers.SerializerMethodField()

    # print('teacher :' , teacher)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'courses', 'course_name', 'teacher', 'teacher_name', 'start_date', 'end_date']
        
    def get_course_name(self, obj):
        return [course.name for course in obj.courses.all()]
        # return [course.name for course in obj.courses.all()]
    
    def get_teacher_name(self, obj):
        return obj.teacher.username

    def create(self , validated_data):
        courses = validated_data.pop('courses')
        classroom = Classroom.objects.create(**validated_data)
        classroom.courses.set(courses)
        return classroom
    
class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(),write_only=True)
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all() , many=True, write_only=True)
    student_name = serializers.SerializerMethodField()
    course_names = serializers.SerializerMethodField()
    # print(' course not convert\n' , courses , '\n')
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_name', 'courses', 'enrollment_date' ,'course_names']

    def get_student_name(self, obj):
        return obj.student.first_name

    def get_course_names(self, obj):
        return [course.name for course in obj.courses.all()]

    def create(self, validated_data):
        courses = validated_data.pop('courses')
        enrollment = Enrollment.objects.create(**validated_data)
        enrollment.courses.set(courses)  # Set the many-to-many field
        return enrollment
    
class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class_instance = ClassroomSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'class_instance', 'date', 'status', 'status_display', 'notes']

class ExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = ['id', 'course', 'class_instance', 'title', 'description', 'exam_date', 'start_time', 'end_time']

class ExamResultSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # exam = ExamSerializer(read_only=True)

    class Meta:
        model = ExamResult
        fields = ['id', 'student', 'exam', 'score', 'grade']

class StudentSerializer(serializers.ModelSerializer):
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    dob = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"] , )
    admission_date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"], required=False)
    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'age',
            'gender',
            'gender_display',
            'dob',
            'pob',
            'nationality',
            'belt_level',
            'phone',
            'email',
            'mother_name',
            'mother_occupation',
            'father_name',
            'father_occupation',
            'address',
            'parent_contact',
            'student_passport',
            'admission_date',
            'branch'
        ]
    # def validate_admission_date(self, value):
    #     if isinstance(value, timezone.datetime):
    #         return value.date()
    #     return value or timezone.now().date()

class TrailSerializer(serializers.ModelSerializer):
    programs = serializers.PrimaryKeyRelatedField(many=True, queryset=Program.objects.all())
    assign_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    handle_by = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Trail
        fields = [
            'id',
            'client',
            'phone',
            'number_student',
            'programs',
            'status',
            'status_display',
            'assign_by',
            'handle_by'
        ]

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [ 'id', 'student', 'class_instance', 'date' , 'status', 'notes' ]

