import django_filters
from .models import User  # Replace with your actual User model import

class UserFilter(django_filters.FilterSet):
    role_name = django_filters.CharFilter(field_name='roles__name', lookup_expr='iexact')  # Case-insensitive exact match
    role_id = django_filters.NumberFilter(field_name='roles__id')

    class Meta:
        model = User
        fields = ['role_name' , 'role_id']
