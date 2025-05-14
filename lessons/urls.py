from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('', views.LessonViewSet, basename='lesson')

urlpatterns = [
    path('progress/', views.mark_lesson_complete, name='mark-complete'),
    path('exercise/<int:pk>/check/', views.check_exercise, name='check-exercise'),
]

urlpatterns += router.urls