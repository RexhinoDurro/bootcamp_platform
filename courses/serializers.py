# courses/serializers.py
from rest_framework import serializers
from .models import Course, Module
from users.serializers import UserProfileSerializer

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'title', 'description', 'order')

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserProfileSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'description', 'instructor', 
                  'thumbnail', 'created_at', 'updated_at', 'is_published', 'modules')