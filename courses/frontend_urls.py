# courses/frontend_urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course-list'),
    path('courses/<slug:slug>/', views.course_detail, name='course-detail'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]