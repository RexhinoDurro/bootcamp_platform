# JavaScript Bootcamp Platform

A full-featured online learning platform for teaching JavaScript programming, built with Django, Django REST Framework, and vanilla JavaScript.

## Features

### For Students
- **Course Catalog**: Browse available courses and preview course content
- **User Dashboard**: Track your enrolled courses and learning progress
- **Interactive Lessons**: Learn through text, video, and interactive code exercises
- **Progress Tracking**: Save your learning progress as you complete lessons
- **Code Exercises**: Write, run, and submit JavaScript code right in your browser

### For Instructors
- **Course Management**: Create, edit, and publish your own JavaScript courses
- **Content Builder**: Structure your course with modules and lessons
- **Exercise Creator**: Create coding exercises with tests to validate student solutions
- **Student Tracking**: Monitor student progress and completion rates
- **Intuitive Interface**: No coding knowledge required to create courses

## Tech Stack

- **Backend**: Django 5.2, Django REST Framework
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Database**: SQLite (for development)
- **Authentication**: Token-based authentication

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/javascript-bootcamp.git
cd javascript-bootcamp
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser for admin access:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/ in your browser

## Project Structure

- **users**: User authentication and profiles
- **courses**: Course management and organization
- **lessons**: Lesson content, exercises, and progress tracking
- **static**: CSS, JavaScript, and other static files
- **templates**: HTML templates for the frontend

## API Endpoints

### Authentication
- `POST /api/users/register/`: Register a new user
- `POST /api/users/login/`: Log in a user and get an authentication token
- `POST /api/users/logout/`: Log out a user (invalidate token)

### Courses
- `GET /api/courses/`: List all published courses
- `GET /api/courses/{id}/`: Get details of a specific course
- `POST /api/courses/`: Create a new course (instructors only)
- `PUT/PATCH /api/courses/{id}/`: Update a course (instructors only)
- `DELETE /api/courses/{id}/`: Delete a course (instructors only)
- `POST /api/courses/{id}/enroll/`: Enroll in a course
- `GET /api/courses/enrolled/`: List all enrolled courses for the current user

### Lessons
- `GET /api/lessons/?module={module_id}`: List all lessons in a module
- `GET /api/lessons/{id}/`: Get details of a specific lesson
- `POST /api/lessons/`: Create a new lesson (instructors only)
- `PUT/PATCH /api/lessons/{id}/`: Update a lesson (instructors only)
- `DELETE /api/lessons/{id}/`: Delete a lesson (instructors only)
- `POST /api/lessons/progress/`: Mark a lesson as complete
- `POST /api/lessons/exercise/{id}/check/`: Check an exercise solution

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Built with Django and Django REST Framework
- Code syntax highlighting with Prism.js
- Icons from [recommended icon library]