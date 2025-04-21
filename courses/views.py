from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Module
from .serializers import CourseSerializer, ModuleSerializer

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
    
    @action(detail=True, methods=['get'])
    def modules(self, request, pk=None):
        course = self.get_object()
        modules = course.modules.all()
        serializer = ModuleSerializer(modules, many=True)
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
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required
def user_dashboard(request):
    if request.user.is_instructor:
        # For instructors, show their courses
        courses = Course.objects.filter(instructor=request.user)
    else:
        # For students, show enrolled courses (we'll implement enrollment later)
        courses = Course.objects.filter(is_published=True)
        
    return render(request, 'courses/dashboard.html', {'courses': courses})

def login_view(request):
    return render(request, 'users/login.html')

def register_view(request):
    return render(request, 'users/register.html')

def logout_view(request):
    # This will just render a template, actual logout happens via API
    return render(request, 'users/logout.html')