# lessons/serializers.py
from rest_framework import serializers
from .models import Lesson, Exercise, UserProgress

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ('id', 'title', 'description', 'initial_code')
        # Note: solution_code and test_code are excluded for security

class LessonSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'content', 'lesson_type', 'order', 'exercises')

class UserProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    
    class Meta:
        model = UserProgress
        fields = ('id', 'lesson', 'lesson_title', 'completed', 'completed_at')