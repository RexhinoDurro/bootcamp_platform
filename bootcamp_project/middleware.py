# Create a new file in bootcamp_project/middleware.py
import re
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token

class TokenAuthMiddleware:
    """
    Custom middleware to authenticate users via token in the browser.
    This helps bridge the gap between DRF token authentication and Django's session authentication.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Check if user is already authenticated via session
        if request.user.is_authenticated:
            return self.get_response(request)
            
        # Try to authenticate via Authorization header (for API requests)
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                request.user = token.user
            except Token.DoesNotExist:
                pass
                
        # For browser requests, check local storage via JavaScript
        # This would require frontend support to pass token in a custom header
                
        return self.get_response(request)
    
class CSRFExemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.csrf_exempt_urls = [
            re.compile(r'^/api/users/register/$'),
            re.compile(r'^/api/users/login/$'),
            re.compile(r'^/api/users/logout/$'),
            re.compile(r'^/api/courses/\d+/enroll/$'),  # Add this line for enrollment
        ]

    def __call__(self, request):
        # Check if the path matches any of the exempt patterns
        path = request.path_info
        for exempt_url in self.csrf_exempt_urls:
            if exempt_url.match(path):
                request._dont_enforce_csrf_checks = True
                break
        return self.get_response(request)


