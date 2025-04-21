# users/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('profiles', views.UserProfileViewSet, basename='profile')

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_detail, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile-edit'),
]

urlpatterns += router.urls