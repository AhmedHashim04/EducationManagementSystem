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
def create_user_with_profile(username, role):
    user, created = User.objects.get_or_create(username=username, defaults={
        'first_name': username.capitalize(),
        'last_name': "Test",
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
    # مدرس ومدير
    instructor_user, instructor = create_user_with_profile("instructor1", "instructor")
    manager_user, manager = create_user_with_profile("manager1", "assistant")

    # إنشاء طلاب
    student_users_profiles = [
        create_user_with_profile(f"student{i}", "student") for i in range(1, 11)
    ]

    # إنشاء كورسات
    for i in range(10):
        course = Course.objects.create(
            code=f"CSE10{i}",
            name=f"Course {i}",
            description="Test course description",
            credit=random.choice([2.0, 3.0, 4.0]),
            manager=manager,
            instructor=instructor
        )

        # تسجيل الطلاب في الكورس
        for student_user, student in student_users_profiles:
            CourseRegistration.objects.create(
                student=student,
                course=course,
                status=random.choice(['accepted', 'pending', 'rejected'])
            )

        # إنشاء واجبات لكل كورس
        for j in range(3):
            assignment = Assignment.objects.create(
                title=f"Assignment {j} - {course.name}",
                description="This is a test assignment",
                course=course,
                due_date=date.today() + timedelta(days=random.randint(5, 15))
            )

            # حل كل طالب للواجب
            for student_user, student in student_users_profiles:
                solution = Solution.objects.create(
                    assignment=assignment,
                    student=student,
                    content=f"Solution content by {student_user.username} for {assignment.title}"
                )

                # تعيين درجة لكل حل
                Grade.objects.create(
                    solution=solution,
                    score=random.randint(40, 100),
                    feedback=random.choice(["Well done", "Needs improvement", "Excellent work", "Keep trying"])
                )

    print("✅ Added 10 courses, 10 students, assignments, solutions, and grades!")

if __name__ == "__main__":
    populate()
