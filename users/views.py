from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
from .serializers import UserSerializer, UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

# Update the register view
@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Explicitly allow any permissions
@csrf_exempt  # Add CSRF exemption
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        
        # Also log the user in (create a session)
        login(request, user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'is_instructor': user.is_instructor
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt  # Add CSRF exemption
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)  # Create a session
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'is_instructor': user.is_instructor
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])  # Change from IsAuthenticated to AllowAny
@csrf_exempt  # Add CSRF exemption
def user_logout(request):
    try:
        # Delete token if it exists
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
            except:
                pass
            
            # Also log out of the session
            logout(request)
        
        # Clear any remaining session
        if hasattr(request, 'session'):
            request.session.flush()
            
        return Response({'message': 'Successfully logged out'})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Frontend views
def profile_detail(request):
    return render(request, 'users/profile_detail.html')

def profile_edit(request):
    return render(request, 'users/profile_edit.html')