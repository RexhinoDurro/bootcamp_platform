# lessons/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
# from . import views

router = DefaultRouter()
# We'll uncomment this later when you implement the viewset
# router.register('', views.LessonViewSet, basename='lesson')

urlpatterns = [
    # We'll add these view functions later
    # path('progress/', views.mark_lesson_complete, name='mark-complete'),
    # path('exercise/<int:pk>/check/', views.check_exercise, name='check-exercise'),
]

urlpatterns += router.urls