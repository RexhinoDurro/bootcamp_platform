from django.core.management.base import BaseCommand
from django.utils.text import slugify
from users.models import CustomUser
from courses.models import Course, Module, Enrollment
from lessons.models import Lesson, Exercise

class Command(BaseCommand):
    help = 'Creates a sample JavaScript course with modules and lessons'

    def handle(self, *args, **kwargs):
        # Create instructor if needed
        instructor, created = CustomUser.objects.get_or_create(
            username='instructor',
            defaults={
                'email': 'instructor@example.com',
                'is_instructor': True,
                'is_student': False,
                'first_name': 'John',
                'last_name': 'Doe',
                'bio': 'Experienced JavaScript instructor with 10+ years of web development experience.'
            }
        )
        
        if created:
            instructor.set_password('password123')
            instructor.save()
            self.stdout.write(self.style.SUCCESS(f'Created instructor user: {instructor.username}'))
        
        # Create JavaScript course
        course_title = "JavaScript Fundamentals"
        course_slug = slugify(course_title)
        
        course, created = Course.objects.get_or_create(
            slug=course_slug,
            defaults={
                'title': course_title,
                'description': 'Master the fundamentals of JavaScript with this comprehensive course. Learn syntax, functions, objects, arrays, DOM manipulation, and more.',
                'instructor': instructor,
                'is_published': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created course: {course.title}'))
        else:
            self.stdout.write(self.style.WARNING(f'Course already exists: {course.title}'))
            return
        
        # Create modules
        modules_data = [
            {
                'title': 'Getting Started with JavaScript',
                'description': 'Introduction to JavaScript and basic syntax',
                'order': 0,
                'lessons': [
                    {
                        'title': 'Introduction to JavaScript',
                        'content': '<h2>Welcome to JavaScript!</h2><p>JavaScript is a versatile programming language primarily used for web development. It allows you to add interactivity to websites and build full-stack applications.</p><p>In this course, you\'ll learn the fundamentals of JavaScript from the ground up.</p>',
                        'lesson_type': 'text',
                        'order': 0
                    },
                    {
                        'title': 'Setting Up Your Development Environment',
                        'content': '<h2>Development Environment</h2><p>To get started with JavaScript, you need a few essential tools:</p><ul><li>A text editor (like VS Code, Sublime Text, or Atom)</li><li>A modern web browser (Chrome, Firefox, Edge, or Safari)</li><li>Browser developer tools</li></ul><p>That\'s it! JavaScript doesn\'t require any complex setup to get started.</p>',
                        'lesson_type': 'text',
                        'order': 1
                    },
                    {
                        'title': 'Your First JavaScript Program',
                        'content': '<h2>Hello, World!</h2><p>Let\'s write your first JavaScript program. The traditional first program is a simple "Hello, World!" message.</p><p>You can use the <code>console.log()</code> function to output text to the browser\'s console:</p><pre><code>console.log("Hello, World!");</code></pre><p>Try it out in the exercise below!</p>',
                        'lesson_type': 'exercise',
                        'order': 2,
                        'exercises': [
                            {
                                'title': 'Hello World Exercise',
                                'description': 'Write a JavaScript statement that prints "Hello, JavaScript!" to the console.',
                                'initial_code': '// Write your code here\n\n',
                                'solution_code': 'console.log("Hello, JavaScript!");',
                                'test_code': 'function testSolution() {\n  // Mock console.log to capture output\n  let output = "";\n  const originalLog = console.log;\n  console.log = function(msg) { output = msg; };\n  \n  // Run user code\n  try {\n    eval(userCode);\n  } catch(e) {\n    console.log = originalLog;\n    return false;\n  }\n  \n  // Restore console.log\n  console.log = originalLog;\n  \n  // Check result\n  return output === "Hello, JavaScript!";\n}'
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'JavaScript Basics',
                'description': 'Learn about variables, data types, and operators',
                'order': 1,
                'lessons': [
                    {
                        'title': 'Variables and Constants',
                        'content': '<h2>Variables in JavaScript</h2><p>Variables are containers for storing data values. In modern JavaScript, we declare variables using <code>let</code> and constants using <code>const</code>.</p><h3>Using let</h3><pre><code>let name = "John";\nlet age = 30;\nlet isStudent = true;</code></pre><h3>Using const</h3><pre><code>const PI = 3.14159;\nconst MAX_SIZE = 100;</code></pre><p>Use <code>const</code> when the value shouldn\'t change, and <code>let</code> when it might.</p>',
                        'lesson_type': 'text',
                        'order': 0
                    },
                    {
                        'title': 'Data Types',
                        'content': '<h2>JavaScript Data Types</h2><p>JavaScript has several built-in data types:</p><ul><li><strong>String</strong>: Text values like "Hello"</li><li><strong>Number</strong>: Numeric values like 42 or 3.14</li><li><strong>Boolean</strong>: true or false</li><li><strong>Null</strong>: Intentional absence of any value</li><li><strong>Undefined</strong>: Variables without assigned values</li><li><strong>Object</strong>: Collections of related data</li><li><strong>Symbol</strong>: Unique identifiers</li></ul><p>JavaScript is a dynamically typed language, which means you don\'t need to specify the data type when declaring variables.</p>',
                        'lesson_type': 'text',
                        'order': 1
                    },
                    {
                        'title': 'Working with Numbers',
                        'content': '<h2>JavaScript Numbers</h2><p>In JavaScript, there\'s only one number type: a 64-bit floating-point value (similar to a double in other languages).</p><pre><code>let integer = 42;\nlet float = 3.14159;\nlet negative = -273.15;\nlet scientific = 5e3; // 5000</code></pre><h3>Arithmetic Operators</h3><ul><li>Addition: <code>+</code></li><li>Subtraction: <code>-</code></li><li>Multiplication: <code>*</code></li><li>Division: <code>/</code></li><li>Remainder: <code>%</code></li><li>Exponentiation: <code>**</code></li></ul>',
                        'lesson_type': 'text',
                        'order': 2
                    },
                    {
                        'title': 'Number Calculator',
                        'content': '<h2>Creating a Simple Calculator</h2><p>Let\'s apply what we\'ve learned about numbers and operators to create a simple calculator function.</p><p>In this exercise, you\'ll create a function that takes two numbers and an operator, then returns the result of the calculation.</p>',
                        'lesson_type': 'exercise',
                        'order': 3,
                        'exercises': [
                            {
                                'title': 'Simple Calculator',
                                'description': 'Create a function called `calculate` that takes three parameters: `a`, `b`, and `operator`. The function should return the result of applying the operator to the two numbers. The operator can be "+", "-", "*", or "/".',
                                'initial_code': '// Create the calculate function\nfunction calculate(a, b, operator) {\n  // Your code here\n}',
                                'solution_code': 'function calculate(a, b, operator) {\n  switch(operator) {\n    case "+":\n      return a + b;\n    case "-":\n      return a - b;\n    case "*":\n      return a * b;\n    case "/":\n      return a / b;\n    default:\n      return "Invalid operator";\n  }\n}',
                                'test_code': 'function testSolution() {\n  try {\n    const tests = [\n      {a: 5, b: 3, op: "+", expected: 8},\n      {a: 5, b: 3, op: "-", expected: 2},\n      {a: 5, b: 3, op: "*", expected: 15},\n      {a: 6, b: 3, op: "/", expected: 2}\n    ];\n    \n    for (const test of tests) {\n      const result = calculate(test.a, test.b, test.op);\n      if (result !== test.expected) {\n        return false;\n      }\n    }\n    return true;\n  } catch(e) {\n    return false;\n  }\n}'
                            }
                        ]
                    }
                ]
            },
            {
                'title': 'Functions and Scope',
                'description': 'Learn how to create and use functions in JavaScript',
                'order': 2,
                'lessons': [
                    {
                        'title': 'Introduction to Functions',
                        'content': '<h2>JavaScript Functions</h2><p>Functions are reusable blocks of code designed to perform specific tasks. They help organize your code and make it more maintainable.</p><h3>Declaring Functions</h3><pre><code>// Function declaration\nfunction greet(name) {\n  return "Hello, " + name + "!";\n}\n\n// Function expression\nconst sayHello = function(name) {\n  return "Hello, " + name + "!";\n};\n\n// Arrow function (ES6)\nconst welcome = (name) => {\n  return "Welcome, " + name + "!";\n};</code></pre><p>Functions can take parameters (inputs) and return values (outputs).</p>',
                        'lesson_type': 'text',
                        'order': 0
                    },
                    {
                        'title': 'Function Parameters and Return Values',
                        'content': '<h2>Parameters and Return Values</h2><p>Functions become powerful when they can accept inputs and provide outputs.</p><h3>Parameters</h3><pre><code>function add(a, b) {\n  return a + b;\n}\n\n// Call the function with arguments\nlet sum = add(5, 3); // sum = 8</code></pre><h3>Default Parameters</h3><pre><code>function greet(name = "Guest") {\n  return "Hello, " + name + "!";\n}\n\ngreet(); // Returns "Hello, Guest!"\ngreet("John"); // Returns "Hello, John!"</code></pre><h3>Return Values</h3><p>The <code>return</code> statement ends function execution and specifies a value to be returned to the function caller.</p>',
                        'lesson_type': 'text',
                        'order': 1
                    },
                    {
                        'title': 'Create a Greeting Function',
                        'content': '<h2>Building a Flexible Greeting Function</h2><p>Let\'s practice creating a function with parameters and return values.</p><p>In this exercise, you\'ll build a greeting function that can customize the message based on the time of day.</p>',
                        'lesson_type': 'exercise',
                        'order': 2,
                        'exercises': [
                            {
                                'title': 'Time-based Greeting',
                                'description': 'Create a function called `getGreeting` that takes a person\'s name and an hour (0-23) as parameters. Return "Good morning, [name]!" if the hour is 5-11, "Good afternoon, [name]!" if the hour is 12-17, and "Good evening, [name]!" if the hour is 18-23 or 0-4.',
                                'initial_code': '// Create the getGreeting function\nfunction getGreeting(name, hour) {\n  // Your code here\n}',
                                'solution_code': 'function getGreeting(name, hour) {\n  if (hour >= 5 && hour <= 11) {\n    return `Good morning, ${name}!`;\n  } else if (hour >= 12 && hour <= 17) {\n    return `Good afternoon, ${name}!`;\n  } else {\n    return `Good evening, ${name}!`;\n  }\n}',
                                'test_code': 'function testSolution() {\n  try {\n    const tests = [\n      {name: "Alice", hour: 8, expected: "Good morning, Alice!"},\n      {name: "Bob", hour: 15, expected: "Good afternoon, Bob!"},\n      {name: "Charlie", hour: 20, expected: "Good evening, Charlie!"},\n      {name: "David", hour: 2, expected: "Good evening, David!"}\n    ];\n    \n    for (const test of tests) {\n      const result = getGreeting(test.name, test.hour);\n      if (result !== test.expected) {\n        return false;\n      }\n    }\n    return true;\n  } catch(e) {\n    return false;\n  }\n}'
                            }
                        ]
                    }
                ]
            }
        ]
        
        # Create the modules and lessons
        for module_data in modules_data:
            module = Module.objects.create(
                course=course,
                title=module_data['title'],
                description=module_data['description'],
                order=module_data['order']
            )
            self.stdout.write(self.style.SUCCESS(f'Created module: {module.title}'))
            
            lessons_data = module_data.pop('lessons', [])
            for lesson_data in lessons_data:
                exercises_data = lesson_data.pop('exercises', [])
                
                lesson = Lesson.objects.create(
                    module=module,
                    **lesson_data
                )
                self.stdout.write(self.style.SUCCESS(f'Created lesson: {lesson.title}'))
                
                for exercise_data in exercises_data:
                    exercise = Exercise.objects.create(
                        lesson=lesson,
                        **exercise_data
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created exercise: {exercise.title}'))
        
        self.stdout.write(self.style.SUCCESS('Sample JavaScript course created successfully!'))