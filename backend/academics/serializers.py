from rest_framework import serializers
from academics.models import *
from authentication.models import User
from school.models import School, Branch

class CourseSerializer(serializers.ModelSerializer):
    program = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all())

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'description', 'credits', 'program', ]
        
class ProgramSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True, write_only=True , required=False)  # Accept primary keys for courses
    course_list = serializers.SerializerMethodField()  # Display courses associated with the program

    class Meta:
        model = Program
        fields = ['id', 'name', 'description', 'branch', 'courses', 'course_list']  # Added course_list to fields

    def get_course_list(self, obj):
        # This will return a list of course names associated with the program
        return [course.name for course in obj.courses.all()]  # Assuming Course has a 'name' field

    def create(self, validated_data):
        courses = validated_data.pop('courses', [])
        program = Program.objects.create(**validated_data)
        program.courses.set(courses)  # Assign the courses to the program
        return program

    def update(self, instance, validated_data):
        courses = validated_data.pop('courses', None)
        instance = super().update(instance, validated_data)
        if courses is not None:
            instance.courses.set(courses)  # Update the courses if provided
        return instance

class ClassroomSerializer(serializers.ModelSerializer):
    
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all() ,many=True )
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(roles=3))
    course_name = serializers.SerializerMethodField()
    teacher_name = serializers.SerializerMethodField()
    student_names = serializers.SerializerMethodField()  # Custom field to get student names
    student_count = serializers.SerializerMethodField()   # Count of students

    # print('teacher :' , teacher)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'courses', 'course_name', 'teacher', 'teacher_name','start_time','end_time', 'start_date', 'end_date',
                              'student_names' , 'student_count'
]
    
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        # Check if start_date is before end_date
        if start_date and start_time and start_time < end_time:
            raise serializers.ValidationError("Start time must be before end time.")
    
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("Start date must be before end date.")
        return data

    def get_course_name(self, obj):
        return [course.name for course in obj.courses.all()]
        # return [course.name for course in obj.courses.all()]
    
    def get_student_names(self, obj):
        # Extract only the first and last names of students
        return [f"{student.first_name} {student.last_name}" for student in obj.students.all()]

    def get_student_count(self, obj):
        return obj.students.count()  # Count all students in this classroom


    
    def get_teacher_name(self, obj):
        return obj.teacher.username

    def create(self , validated_data):
        courses = validated_data.pop('courses')
        classroom = Classroom.objects.create(**validated_data)
        classroom.courses.set(courses)
        return classroom
    
    def update(self, instance, validated_data):
        courses = validated_data.pop('courses', None)  # Pop courses from validated_data
        instance = super().update(instance, validated_data)
        if courses is not None:
            instance.courses.set(courses)  # Update the courses if provided
        return instance
    
class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(),write_only=True)
    # courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all() , many=True, write_only=True)
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
            student = validated_data['student']
            courses = validated_data['courses']

            # Check if enrollment already exists for the student and the courses
            for course in courses:
                if Enrollment.objects.filter(student=student, courses=course).exists():
                    raise serializers.ValidationError(f'Student {student} is already enrolled in {course.name}.')

            # If no duplicates, create the enrollment
            enrollment = Enrollment.objects.create(student=student)
            enrollment.courses.set(courses)  # Set the many-to-many relationship
            return enrollment
    
class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    student_name = serializers.SerializerMethodField()
    class_instance = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())  
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class_name = serializers.SerializerMethodField()  # New field to display class name


    class Meta:
        model = Attendance
        fields = ['id', 'student','student_name', 'class_instance','class_name', 'date', 'status', 'status_display', 'notes']

    def validate(self, data):
        date = data.get("date")
        print("\n date" , date , "\n")

        if date is None:
            raise serializers.ValidationError("Attendance date is required.")
        
        if date < timezone.now().date():
            raise serializers.ValidationError("Attendence date cannot be in the past. ")
        
        return data
    
    def get_class_name(self , obj):
        return obj.class_instance.name 
    
    def get_student_name(self , obj):
        return obj.student.last_name 
    
class ExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = ['id', 'course', 'class_instance', 'title', 'description', 'exam_date', 'start_time', 'end_time']

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        exam_date = data.get('exam_date')
        # Check if start_date is before end_date
        if start_time and end_time > end_time:
            raise serializers.ValidationError("Start date must be before end date.")
        if exam_date < timezone.now().date():
            raise serializers.ValidationError("Exam date cannot be in the past.")
        return data
    
class ExamResultSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    student_names = serializers.SerializerMethodField()  # Custom field to get student names

    # exam = ExamSerializer(read_only=True)

    class Meta:
        model = ExamResult
        fields = ['id', 'student','student_names', 'exam', 'score', 'grade']

    def get_student_names(self, obj):
        # Extract only the first and last names of students
        return obj.student.first_name


class StudentSerializer(serializers.ModelSerializer):

    classrooms = ClassroomSerializer(many=True, read_only=True)  # Show classroom details in student data
    classroom_ids = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), many=True, source='classrooms', write_only=True)  # For assigning multiple classrooms by id
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
            'branch',
            'image',
            'classrooms', 'classroom_ids'
        ]
    def get_course(self, obj):
            enrollments = Enrollment.objects.filter(student=obj)

            # Get the courses the student is enrolled in through the enrollment model
            return CourseSerializer(obj.courses.all(), many=True).data

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

class AddStudentsToClassroomSerializer(serializers.ModelSerializer):
    student_ids = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True, write_only=True , )

    class Meta:
        model = Classroom
        fields = ['student_ids']

    def update(self, instance, validated_data):
        # Get the list of students to add to the classroom
        student_ids = validated_data.pop('student_ids')
        
        # Add the students to the classroom
        instance.students.add(*student_ids)
        
        # Save the updated classroom instance
        instance.save()
        return instance
    

        

