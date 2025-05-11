# courses/frontend_urls.py
from django.urls import path
from . import views
from lessons import views as lesson_views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course-list'),
    path('courses/<slug:slug>/', views.course_detail, name='course-detail'),
    
    # Auth pages
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Learner dashboard
    path('dashboard/', views.user_dashboard, name='dashboard'),
    
    # Course content pages
    path('courses/<slug:slug>/learn/', lesson_views.course_content, name='course-content'),
    path('lessons/<int:lesson_id>/', lesson_views.lesson_detail, name='lesson-detail'),
    
    # Instructor pages
    path('dashboard/instructor/', views.instructor_dashboard, name='instructor-dashboard'),
    path('courses/create/', views.course_create, name='course-create'),
    path('courses/edit/<int:course_id>/', views.course_edit, name='course-edit'),
    path('courses/modules/<int:course_id>/', views.module_management, name='module-management'),
    path('courses/modules/<int:module_id>/lessons/', lesson_views.lesson_management, name='lesson-management'),
    path('lessons/<int:lesson_id>/exercises/', lesson_views.exercise_management, name='exercise-management'),
]