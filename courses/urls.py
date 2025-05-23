# courses/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.CourseViewSet, basename='course')

urlpatterns = [
    path('enrolled/', views.get_enrolled_courses, name='enrolled-courses'),
]

urlpatterns += router.urls