import os
import sys
import django
import random
from datetime import timedelta, date
from django.utils import timezone

# إعداد Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from django.contrib.auth.models import User
from account.models import Profile
from course.models import Course, CourseRegistration
from assignment.models import Assignment, Solution, Grade

# إنشاء يوزرات
def create_user_with_profile(username, first_name, last_name, role):
    user, created = User.objects.get_or_create(username=username, defaults={
        'first_name': first_name,
        'last_name': last_name,
        'email': f"{username}@example.com"
    })
    if created:
        user._role = role
        user.save()
    profile = Profile.objects.get(user=user)
    profile.role = role
    profile.save()
    return user, profile

def populate():
    # Create instructors
    instructors_data = [
        ("ahmad_ali", "Ahmad", "Ali", "instructor"),
        ("sarah_khan", "Sarah", "Khan", "instructor"),
        ("mohammed_hassan", "Mohammed", "Hassan", "instructor")
    ]
    instructors = [create_user_with_profile(*data) for data in instructors_data]

    # Create students with realistic names
    student_data = [
        ("abdullah_omar", "Abdullah", "Omar", "student"),
        ("fatima_ahmed", "Fatima", "Ahmed", "student"),
        ("omar_khalid", "Omar", "Khalid", "student"),
        ("layla_ibrahim", "Layla", "Ibrahim", "student"),
        ("yusuf_ali", "Yusuf", "Ali", "student"),
        ("noor_hassan", "Noor", "Hassan", "student"),
        ("zainab_mahmoud", "Zainab", "Mahmoud", "student"),
        ("ahmed_saeed", "Ahmed", "Saeed", "student"),
        ("mariam_tariq", "Mariam", "Tariq", "student"),
        ("hassan_qadir", "Hassan", "Qadir", "student"),
        ("aisha_malik", "Aisha", "Malik", "student"),
        ("karim_rashid", "Karim", "Rashid", "student"),
        ("sara_mansour", "Sara", "Mansour", "student"),
        ("mohammad_qasim", "Mohammad", "Qasim", "student"),
        ("leila_hamid", "Leila", "Hamid", "student")
    ]
    student_users_profiles = [create_user_with_profile(*data) for data in student_data]

    # Create courses with realistic names and descriptions
    courses_data = [
        {
            "code": "CSE101",
            "name": "Introduction to Programming",
            "description": "Fundamentals of programming using Python, covering basic syntax, data structures, and algorithms",
            "credit": 3.0
        },
        {
            "code": "CSE201",
            "name": "Data Structures and Algorithms",
            "description": "Advanced programming concepts including sorting algorithms, trees, and graphs",
            "credit": 4.0
        },
        {
            "code": "CSE301",
            "name": "Database Systems",
            "description": "Introduction to database design, SQL, and database management systems",
            "credit": 3.0
        },
        {
            "code": "CSE401",
            "name": "Web Development",
            "description": "Full-stack web development using modern frameworks and technologies",
            "credit": 4.0
        },
        {
            "code": "CSE501",
            "name": "Artificial Intelligence",
            "description": "Introduction to AI concepts, machine learning, and neural networks",
            "credit": 4.0
        },
        {
            "code": "CSE601",
            "name": "Cybersecurity Fundamentals",
            "description": "Basic concepts of network security, cryptography, and secure system design",
            "credit": 3.0
        },
        {
            "code": "CSE701",
            "name": "Mobile App Development",
            "description": "Development of mobile applications for iOS and Android platforms",
            "credit": 3.0
        }
    ]

    for course_data in courses_data:
        course = Course.objects.create(
            code=course_data["code"],
            name=course_data["name"],
            description=course_data["description"],
            credit=course_data["credit"],
            instructor=random.choice(instructors)[1]
        )

        # Register students in the course
        for student_user, student in student_users_profiles:
            CourseRegistration.objects.create(
                student=student,
                course=course,
                status='accepted'
            )

        # Create assignments for each course
        assignments_data = [
            ("Project Proposal", "Submit a detailed proposal for your final project including objectives and timeline"),
            ("Mid-term Assignment", "Complete the practical implementation of concepts covered in weeks 1-7"),
            ("Research Paper", "Write a research paper on an advanced topic related to the course"),
            ("Group Project", "Work in teams to develop a comprehensive solution to a real-world problem"),
            ("Final Project", "Individual project implementing all major concepts covered in the course"),
            ("Technical Documentation", "Create detailed documentation for your implemented solution"),
            ("Practical Lab Work", "Complete hands-on exercises in the lab environment")
        ]

        for j, (title, desc) in enumerate(assignments_data):
            assignment = Assignment.objects.create(
                title=f"{title} - {course.name}",
                description=desc,
                course=course,
                due_date=date.today() + timedelta(days=random.randint(5, 30))
            )

            # Create solutions for each student
            for student_user, student in student_users_profiles:
                solution = Solution.objects.create(
                    assignment=assignment,
                    student=student,
                    content=f"Detailed solution implementation by {student_user.first_name} for {assignment.title}"
                )

                # Grade each solution
                Grade.objects.create(
                    solution=solution,
                    score=random.randint(65, 100),
                    feedback=random.choice([
                        "Excellent work! Your implementation shows great understanding of the concepts.",
                        "Good effort, but there's room for improvement in code optimization.",
                        "Very well structured solution. Consider adding more documentation.",
                        "Strong technical implementation. Work on error handling.",
                        "Outstanding work! Your solution exceeded expectations."
                    ])
                )

    print("✅ Successfully populated the database with realistic courses, students, assignments, solutions, and grades!")

if __name__ == "__main__":
    populate()
