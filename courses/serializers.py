# courses/serializers.py
from rest_framework import serializers
from .models import Course, Module, Enrollment
from users.serializers import UserProfileSerializer

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'title', 'description', 'order')

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserProfileSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    is_enrolled = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ('id', 'title', 'slug', 'description', 'instructor', 
                  'thumbnail', 'created_at', 'updated_at', 'is_published', 
                  'modules', 'is_enrolled')
    
    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(student=request.user, course=obj, is_active=True).exists()
        return False

class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ('id', 'course', 'course_title', 'enrolled_at', 'is_active')