// static/js/auth.js

const Auth = {
  // Check if user is authenticated
  isAuthenticated: function() {
    return localStorage.getItem('authToken') !== null;
  },
  
  // Get authentication token
  getToken: function() {
    return localStorage.getItem('authToken');
  },
  
  // Set authentication token and user info
  setAuth: function(token, userId, username, isInstructor) {
    localStorage.setItem('authToken', token);
    localStorage.setItem('userId', userId);
    localStorage.setItem('username', username);
    localStorage.setItem('isInstructor', isInstructor);
  },
  
  // Clear all authentication data
  clearAuth: function() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    localStorage.removeItem('isInstructor');
  },
  
  // Check if user is an instructor
  isInstructor: function() {
    return localStorage.getItem('isInstructor') === 'true';
  },
  
  // Get current username
  getUsername: function() {
    return localStorage.getItem('username');
  },
  
  // Get user ID
  getUserId: function() {
    return localStorage.getItem('userId');
  },
  
  // Make authenticated API request
  apiRequest: async function(url, method = 'GET', data = null) {
    const headers = {
      'Content-Type': 'application/json'
    };
    
    if (this.isAuthenticated()) {
      headers['Authorization'] = `Token ${this.getToken()}`;
    }
    
    const options = {
      method: method,
      headers: headers
    };
    
    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
      options.body = JSON.stringify(data);
    }
    
    try {
      const response = await fetch(url, options);
      const responseData = await response.json();
      
      return {
        success: response.ok,
        status: response.status,
        data: responseData
      };
    } catch (error) {
      console.error('API request error:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
};

// Add event listener for page load to check authentication
document.addEventListener('DOMContentLoaded', function() {
  const authElements = document.querySelectorAll('[data-auth-required]');
  const nonAuthElements = document.querySelectorAll('[data-non-auth]');
  const instructorElements = document.querySelectorAll('[data-instructor-only]');
  
  if (Auth.isAuthenticated()) {
    // Show elements that require authentication
    authElements.forEach(element => {
      element.style.display = '';
    });
    
    // Hide elements for non-authenticated users
    nonAuthElements.forEach(element => {
      element.style.display = 'none';
    });
    
    // Show or hide instructor-only elements
    instructorElements.forEach(element => {
      element.style.display = Auth.isInstructor() ? '' : 'none';
    });
    
    // Update username in username elements
    document.querySelectorAll('[data-username]').forEach(element => {
      element.textContent = Auth.getUsername();
    });
  } else {
    // Hide elements that require authentication
    authElements.forEach(element => {
      element.style.display = 'none';
    });
    
    // Show elements for non-authenticated users
    nonAuthElements.forEach(element => {
      element.style.display = '';
    });
    
    // Hide instructor-only elements
    instructorElements.forEach(element => {
      element.style.display = 'none';
    });
  }
});