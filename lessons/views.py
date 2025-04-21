from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .models import Lesson, Exercise, UserProgress
from .serializers import LessonSerializer, ExerciseSerializer, UserProgressSerializer
from courses.models import Module

class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        module_id = self.request.query_params.get('module', None)
        if module_id:
            module = get_object_or_404(Module, id=module_id)
            return Lesson.objects.filter(module=module)
        return Lesson.objects.all()
    
    @action(detail=True, methods=['get'])
    def exercises(self, request, pk=None):
        lesson = self.get_object()
        exercises = lesson.exercises.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        lesson = self.get_object()
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )
        serializer = UserProgressSerializer(progress)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_lesson_complete(request):
    lesson_id = request.data.get('lesson_id')
    if not lesson_id:
        return Response({'error': 'Lesson ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()
    
    return Response({'success': True, 'message': 'Lesson marked as complete'})

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def check_exercise(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    user_code = request.data.get('code', '')
    
    # In a real implementation, you would run tests against the user's code
    # For now, we'll just check if the code contains certain keywords
    
    # Simple placeholder validation - in production, you'd use something more robust
    # like a sandboxed code execution environment
    success = False
    feedback = "Your solution doesn't seem to meet the requirements."
    
    if len(user_code) > 0 and any(keyword in user_code for keyword in ['function', 'const', 'let', 'var']):
        success = True
        feedback = "Great job! Your solution passes the tests."
        
        # Mark the lesson as complete
        lesson = exercise.lesson
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )
        progress.completed = True
        progress.completed_at = timezone.now()
        progress.save()
    
    return Response({
        'success': success,
        'feedback': feedback
    })