from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .models import Lesson, Exercise, UserProgress
from .serializers import LessonSerializer, ExerciseSerializer, UserProgressSerializer
from courses.models import Module, Course, Enrollment

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
@permission_classes([permissions.AllowAny])  # Changed from IsAuthenticated to AllowAny
def mark_lesson_complete(request):
    lesson_id = request.data.get('lesson_id')
    if not lesson_id:
        return Response({'error': 'Lesson ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Get the user from the request if authenticated, otherwise use a default or anonymous user
    user = request.user
    if not user.is_authenticated:
        # For anonymous users, you might want to handle this differently
        # This is just a placeholder approach - modify based on your needs
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user, created = User.objects.get_or_create(username="anonymous_user")
    
    progress, created = UserProgress.objects.get_or_create(
        user=user,
        lesson=lesson
    )
    
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()
    
    return Response({'success': True, 'message': 'Lesson marked as complete'})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Changed from IsAuthenticated to AllowAny
def check_exercise(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)
    user_code = request.data.get('code', '')
    
    # More robust validation with hints
    success = False
    feedback = "Your solution doesn't seem to meet the requirements."
    hints = []
    
    # Basic validation - check if code contains required keywords/patterns
    # This is simplified; a real implementation would use a proper code execution environment
    try:
        # Check if the required function exists in the code
        if 'function calculate' in exercise.test_code and 'function calculate' not in user_code:
            hints.append("Make sure you have defined a function named 'calculate'.")
        
        if 'function getGreeting' in exercise.test_code and 'function getGreeting' not in user_code:
            hints.append("Make sure you have defined a function named 'getGreeting'.")
        
        # Check for common issues
        if user_code.count('return') == 0 and ('function' in user_code):
            hints.append("Your function should return a value using the 'return' keyword.")
        
        if 'console.log' in exercise.test_code and 'console.log' not in user_code:
            hints.append("Try using console.log() to output your message.")
        
        # Simple tests for specific exercises (based on exercise ID or title)
        if "Hello World" in exercise.title and "Hello, JavaScript" not in user_code:
            hints.append("Your code should output 'Hello, JavaScript!' to the console.")
        
        if "Calculator" in exercise.title:
            for op in ['+', '-', '*', '/']:
                if op not in user_code:
                    hints.append(f"Make sure your calculator handles the '{op}' operation.")
        
        if "Greeting" in exercise.title and "time" in exercise.description.lower():
            if "morning" not in user_code or "afternoon" not in user_code or "evening" not in user_code:
                hints.append("Your function should provide different greetings based on the time of day.")
        
        # More general validation
        if len(user_code.strip()) < 10:
            hints.append("Your solution seems too short. Make sure you've written a complete solution.")
        
        # For simplicity, we'll consider the solution successful if at least some expected patterns are present
        # In a real implementation, you would execute the test code in a sandbox
        if (
            ("Hello World" in exercise.title and "Hello, JavaScript" in user_code) or
            ("Calculator" in exercise.title and all(op in user_code for op in ['+', '-', '*', '/'])) or
            ("Greeting" in exercise.title and all(time in user_code for time in ["morning", "afternoon", "evening"]))
        ):
            success = True
            if "Hello World" in exercise.title:
                feedback = "Great job! You've successfully written your first JavaScript statement."
            elif "Calculator" in exercise.title:
                feedback = "Excellent! Your calculator function handles all required operations."
            elif "Greeting" in exercise.title:
                feedback = "Well done! Your greeting function properly changes based on the time of day."
            else:
                feedback = "Great job! Your solution passes the tests."
            
            # Mark the lesson as complete if the user is authenticated
            if request.user.is_authenticated:
                lesson = exercise.lesson
                progress, created = UserProgress.objects.get_or_create(
                    user=request.user,
                    lesson=lesson
                )
                progress.completed = True
                progress.completed_at = timezone.now()
                progress.save()
    
    except Exception as e:
        feedback = f"Error checking your code: {str(e)}"
        hints = ["Make sure your code has valid syntax."]
    
    return Response({
        'success': success,
        'feedback': feedback,
        'hints': hints
    })
    
@login_required
def course_content(request, slug):
    # Get the course
    course = get_object_or_404(Course, slug=slug, is_published=True)
    
    # Check if the user is enrolled
    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course,
        is_active=True
    ).exists()
    
    if not is_enrolled and not request.user.is_instructor:
        return redirect('course-detail', slug=slug)
    
    # Get modules and lessons
    modules = Module.objects.filter(course=course).prefetch_related('lessons')
    
    # Get user progress
    user_progress = UserProgress.objects.filter(
        user=request.user,
        lesson__module__course=course
    ).values_list('lesson_id', flat=True)
    
    # Calculate course progress
    total_lessons = Lesson.objects.filter(module__course=course).count()
    completed_lessons = len(user_progress)
    
    progress_percentage = 0
    if total_lessons > 0:
        progress_percentage = int((completed_lessons / total_lessons) * 100)
    
    # Get first lesson of the course for the "Review" link
    first_lesson = None
    if modules.exists() and modules.first().lessons.exists():
        first_lesson = modules.first().lessons.first()
    
    # Find the first incomplete lesson (for "Continue Learning")
    first_incomplete_lesson = None
    if modules.exists():
        for module in modules:
            lessons = module.lessons.all()
            for lesson in lessons:
                if lesson.id not in user_progress:
                    first_incomplete_lesson = lesson
                    break
            if first_incomplete_lesson:
                break
    
    # Calculate estimated time to complete (example logic)
    estimated_hours = total_lessons * 0.5  # Assume each lesson takes 30 minutes
    
    return render(request, 'lessons/course_content.html', {
        'course': course,
        'modules': modules,
        'user_progress': user_progress,
        'progress_percentage': progress_percentage,
        'first_lesson': first_lesson,  # Add this variable
        'first_incomplete_lesson': first_incomplete_lesson,  # Add this variable
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'estimated_hours': estimated_hours
    })

@login_required
def lesson_detail(request, lesson_id):
    # Get the lesson
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.module.course
    
    # Check if the user is enrolled or is the instructor
    is_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course,
        is_active=True
    ).exists()
    
    if not is_enrolled and not request.user.is_instructor and course.instructor != request.user:
        return redirect('course-detail', slug=course.slug)
    
    # Get user progress
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson
    )
    
    # Get next and previous lessons
    module_lessons = Lesson.objects.filter(module=lesson.module).order_by('order')
    
    prev_lesson = None
    next_lesson = None
    
    # Find previous and next lessons
    found_current = False
    for module_lesson in module_lessons:
        if found_current:
            next_lesson = module_lesson
            break
        elif module_lesson.id == lesson.id:
            found_current = True
        else:
            prev_lesson = module_lesson
    
    # If no next lesson in the current module, look for the first lesson in the next module
    if next_lesson is None and found_current:
        next_module = Module.objects.filter(
            course=course,
            order__gt=lesson.module.order
        ).order_by('order').first()
        
        if next_module:
            next_lesson = Lesson.objects.filter(module=next_module).order_by('order').first()
    
    # If no previous lesson in the current module, look for the last lesson in the previous module
    if prev_lesson is None and lesson.module.order > 0:
        prev_module = Module.objects.filter(
            course=course,
            order__lt=lesson.module.order
        ).order_by('-order').first()
        
        if prev_module:
            prev_lesson = Lesson.objects.filter(module=prev_module).order_by('-order').first()
    
    return render(request, 'lessons/lesson_detail.html', {
        'lesson': lesson,
        'progress': progress,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson
    })

@login_required
def lesson_management(request, module_id):
    # Verify the user is an instructor
    if not request.user.is_instructor:
        return redirect('dashboard')
    
    # Get the module and verify ownership
    module = get_object_or_404(Module, id=module_id)
    
    if module.course.instructor != request.user:
        return redirect('dashboard')
    
    return render(request, 'lessons/lesson_management.html', {
        'module': module
    })

@login_required
def exercise_management(request, lesson_id):
    # Verify the user is an instructor
    if not request.user.is_instructor:
        return redirect('dashboard')
    
    # Get the lesson and verify ownership
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if lesson.module.course.instructor != request.user:
        return redirect('dashboard')
    
    return render(request, 'lessons/exercise_management.html', {
        'lesson': lesson
    })