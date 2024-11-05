import django_filters
from .models import Program , Course , Student , Attendance


class ProgramFilter(django_filters.FilterSet):
    # Filter by Program ID
    id = django_filters.NumberFilter(field_name='id')
    # Filter by Program Name
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # Case-insensitive partial match

    class Meta:
        model = Program
        fields = ['id', 'name']

class CourseFilter(django_filters.FilterSet):
    program = django_filters.NumberFilter(field_name='program__id')  # Filter by program ID

    class Meta:
        model = Course
        fields = ['program']  # Expose the 'program' field as a filter


class StudentFilter(django_filters.FilterSet):
    classroom = django_filters.NumberFilter(field_name='classrooms__id')  # Filter by Classroom ID

    class Meta:
        model = Student
        fields = ['classroom']  # Expose the 'classroom' field as a 

class AttendanceFilter(django_filters.FilterSet):
    student = django_filters.NumberFilter(field_name='student_id')

    class Meta:
        model = Attendance
        fields = ['student']