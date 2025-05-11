from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Exists, OuterRef
from .models import Course, Module, Enrollment
from lessons.models import Lesson, UserProgress
from .serializers import CourseSerializer, ModuleSerializer, EnrollmentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
    
    def get_queryset(self):
        # If user is not authenticated, show only published courses
        if not self.request.user.is_authenticated:
            return Course.objects.filter(is_published=True)
        
        # If user is instructor, show their courses (published or not)
        if self.request.user.is_instructor:
            return Course.objects.filter(instructor=self.request.user)
            
        # For students, show all published courses
        return Course.objects.filter(is_published=True)
    
    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    @action(detail=True, methods=['get'])
    def modules(self, request, pk=None):
        course = self.get_object()
        modules = course.modules.all()
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    @permission_classes([permissions.IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        student = request.user
        
        # Check if already enrolled
        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response({'error': 'Already enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create enrollment
        enrollment = Enrollment.objects.create(student=student, course=course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    @permission_classes([permissions.IsAuthenticated])
    def unenroll(self, request, pk=None):
        course = self.get_object()
        student = request.user
        
        try:
            enrollment = Enrollment.objects.get(student=student, course=course)
            enrollment.is_active = False
            enrollment.save()
            return Response({'message': 'Successfully unenrolled'})
        except Enrollment.DoesNotExist:
            return Response({'error': 'Not enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_enrolled_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user, is_active=True)
    courses = [enrollment.course for enrollment in enrollments]
    serializer = CourseSerializer(courses, many=True, context={'request': request})
    return Response(serializer.data)

# Frontend views
def home(request):
    featured_courses = Course.objects.filter(is_published=True).order_by('-created_at')[:3]
    return render(request, 'courses/home.html', {'featured_courses': featured_courses})

def course_list(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    # Check if user is enrolled
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(
            student=request.user, 
            course=course,
            is_active=True
        ).exists()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled
    })

@login_required
def user_dashboard(request):
    if request.user.is_instructor:
        # For instructors, show their courses
        courses = Course.objects.filter(instructor=request.user)
    else:
        # For students, show enrolled courses
        enrollments = Enrollment.objects.filter(student=request.user, is_active=True)
        courses = [enrollment.course for enrollment in enrollments]
        
    return render(request, 'courses/dashboard.html', {'courses': courses})

def login_view(request):
    return render(request, 'users/login.html')

def register_view(request):
    return render(request, 'users/register.html')

def logout_view(request):
    # This will just render a template, actual logout happens via API
    return render(request, 'users/logout.html')

@login_required
def instructor_dashboard(request):
    # Verify the user is an instructor
    if not request.user.is_instructor:
        return redirect('dashboard')
    
    # Get the instructor's courses
    courses = Course.objects.filter(instructor=request.user)
    
    # Get total students enrolled in the instructor's courses
    total_students = Enrollment.objects.filter(
        course__instructor=request.user,
        is_active=True
    ).values('student').distinct().count()
    
    # Get total course completions
    course_completions = UserProgress.objects.filter(
        lesson__module__course__instructor=request.user,
        completed=True
    ).count()
    
    return render(request, 'courses/instructor_dashboard.html', {
        'courses': courses,
        'total_students': total_students,
        'course_completions': course_completions
    })

@login_required
def course_create(request):
    # Verify the user is an instructor
    if not request.user.is_instructor:
        return redirect('dashboard')
    
    return render(request, 'courses/course_form.html', {
        'is_edit': False
    })

@login_required
def course_edit(request, course_id):
    # Verify the user is an instructor
    if not request.user.is_instructor:
        return redirect('dashboard')
    
    # Get the course and verify ownership
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    return render(request, 'courses/course_form.html', {
        'is_edit': True,
        'course': course
    })

@login_required
def module_management(request, course_id):
    # Verify the user is an instructor
    if not request.user.is_instructor:
        return redirect('dashboard')
    
    # Get the course and verify ownership
    course = get_object_or_404(Course, id=course_id, instructor=request.user)
    
    return render(request, 'courses/module_management.html', {
        'course': course
    })