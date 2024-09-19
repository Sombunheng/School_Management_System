from rest_framework.serializers import ModelSerializer
from authentication.models import User
from todos.models import Todo
from rest_framework import serializers

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id' ,'title' , 'desc' , 'is_complete' , 'created_at', )