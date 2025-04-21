// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
  console.log('JavaScript Bootcamp Platform loaded!');
  
  // Global navigation enhancements
  const navLinks = document.querySelectorAll('.main-nav a');
  
  navLinks.forEach(link => {
      if (link.getAttribute('href') === window.location.pathname) {
          link.classList.add('active');
      }
  });
  
  // Form validation for all forms
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
      form.addEventListener('submit', function(e) {
          const requiredFields = form.querySelectorAll('[required]');
          let isValid = true;
          
          requiredFields.forEach(field => {
              if (!field.value.trim()) {
                  isValid = false;
                  // Add error class and message
                  field.classList.add('is-invalid');
                  
                  // Create error message if it doesn't exist
                  let errorMsg = field.nextElementSibling;
                  if (!errorMsg || !errorMsg.classList.contains('error-message')) {
                      errorMsg = document.createElement('div');
                      errorMsg.classList.add('error-message');
                      errorMsg.textContent = 'This field is required';
                      field.parentNode.insertBefore(errorMsg, field.nextSibling);
                  }
              } else {
                  field.classList.remove('is-invalid');
                  // Remove error message if it exists
                  const errorMsg = field.nextElementSibling;
                  if (errorMsg && errorMsg.classList.contains('error-message')) {
                      errorMsg.remove();
                  }
              }
          });
          
          if (!isValid) {
              e.preventDefault();
          }
      });
  });
});

// Function to handle dynamic content loading
function loadContent(url, targetElement) {
  const contentArea = document.querySelector(targetElement);
  
  fetch(url)
      .then(response => {
          if (!response.ok) {
              throw new Error('Network response was not ok');
          }
          return response.json();
      })
      .then(data => {
          if (contentArea) {
              // Process and display the data as needed
              contentArea.innerHTML = ''; // Clear existing content
              
              // Example of how to handle different data types
              if (Array.isArray(data)) {
                  data.forEach(item => {
                      const itemElement = createElementFromData(item);
                      contentArea.appendChild(itemElement);
                  });
              } else {
                  const itemElement = createElementFromData(data);
                  contentArea.appendChild(itemElement);
              }
          }
      })
      .catch(error => {
          console.error('Error loading content:', error);
          contentArea.innerHTML = '<p class="error">Failed to load content. Please try again.</p>';
      });
}

// Helper function to create DOM elements from data
function createElementFromData(data) {
  // This will need to be customized based on your data structure
  const element = document.createElement('div');
  element.classList.add('dynamic-item');
  
  // Example structure - modify based on your actual data
  if (data.title) {
      const title = document.createElement('h3');
      title.textContent = data.title;
      element.appendChild(title);
  }
  
  if (data.description) {
      const description = document.createElement('p');
      description.textContent = data.description;
      element.appendChild(description);
  }
  
  return element;
}