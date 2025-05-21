import os
import django
import random
from faker import Faker
from django.contrib.auth.models import User
from django.utils import timezone
from account.models import Profile
from course.models import Course, CourseRegistration, CourseAssistant, CourseMaterial
from assignment.models import Assignment, Solution, Grade
from chat.models import Chat, Message

fake = Faker()

NUM_INSTRUCTORS = 3
NUM_ASSISTANTS = 5
NUM_STUDENTS = 20
NUM_COURSES = 5
NUM_ASSIGNMENTS_PER_COURSE = 3
NUM_SOLUTIONS_PER_ASSIGNMENT = 10
NUM_MESSAGES = 50


def create_users_and_profiles():
    users_profiles = {"instructors": [], "assistants": [], "students": []}
    # Instructors
    for _ in range(NUM_INSTRUCTORS):
        user = User.objects.create_user(username=fake.user_name(), email=fake.email(), password='123456')
        user._role = 'instructor'
        user.save()
        users_profiles["instructors"].append(user.profile)

    # Assistants
    for _ in range(NUM_ASSISTANTS):
        user = User.objects.create_user(username=fake.user_name(), email=fake.email(), password='123456')
        user._role = 'assistant'
        user.save()
        users_profiles["assistants"].append(user.profile)

    # Students
    for _ in range(NUM_STUDENTS):
        user = User.objects.create_user(username=fake.user_name(), email=fake.email(), password='123456')
        user._role = 'student'
        user.save()
        users_profiles["students"].append(user.profile)

    return users_profiles


def create_courses(instructors):
    courses = []
    for _ in range(NUM_COURSES):
        instructor = random.choice(instructors)
        course = Course.objects.create(
            code=fake.unique.bothify(text='CSE###'),
            name=fake.catch_phrase(),
            description=fake.text(),
            instructor=instructor,
            registration_start_at=timezone.now(),
            registration_end_at=timezone.now() + timezone.timedelta(days=30)
        )
        courses.append(course)
    return courses


def register_students_and_assistants(courses, students, assistants):
    for course in courses:
        selected_students = random.sample(students, k=10)
        selected_assistants = random.sample(assistants, k=2)

        for student in selected_students:
            CourseRegistration.objects.create(student=student, course=course)

        for assistant in selected_assistants:
            CourseAssistant.objects.create(course=course, assistant=assistant, permession=random.choice([True, False]))


def create_course_materials(courses):
    for course in courses:
        for _ in range(2):
            CourseMaterial.objects.create(
                course=course,
                title=fake.sentence(),
                description=fake.text(),
                file='course_materials/sample.pdf',
                is_active=True
            )


def create_assignments(courses):
    assignments = []
    for course in courses:
        for _ in range(NUM_ASSIGNMENTS_PER_COURSE):
            assignment = Assignment.objects.create(
                title=fake.unique.sentence(nb_words=4),
                description=fake.paragraph(),
                course=course,
                due_date=timezone.now() + timezone.timedelta(days=random.randint(7, 30))
            )
            assignments.append(assignment)
    return assignments


def create_solutions_and_grades(assignments, students):
    for assignment in assignments:
        selected_students = random.sample(students, k=NUM_SOLUTIONS_PER_ASSIGNMENT)
        for student in selected_students:
            solution = Solution.objects.create(
                assignment=assignment,
                student=student,
                content=fake.paragraph(),
                file_attachment=None
            )
            Grade.objects.create(
                solution=solution,
                score=random.randint(50, 100),
                feedback=fake.sentence()
            )


def create_chats_and_messages(users):
    all_users = User.objects.filter(profile__role__in=['instructor', 'assistant', 'student'])
    for _ in range(10):
        participants = random.sample(list(all_users), 2)
        chat = Chat.objects.create()
        chat.participants.set(participants)
        for _ in range(random.randint(1, 5)):
            Message.objects.create(
                chat=chat,
                sender=random.choice(participants),
                content=fake.sentence(),
                is_read=random.choice([True, False])
            )
def clear_data():
    print("⚠️  Deleting all fake data...")

    # حذف الرسائل والشاتات
    Message.objects.all().delete()
    Chat.objects.all().delete()

    # حذف الدرجات والحلول
    Grade.objects.all().delete()
    Solution.objects.all().delete()

    # حذف التكاليف
    Assignment.objects.all().delete()

    # حذف المواد التعليمية
    CourseMaterial.objects.all().delete()

    # حذف التسجيلات والمساعدين
    CourseRegistration.objects.all().delete()
    CourseAssistant.objects.all().delete()

    # حذف الكورسات
    Course.objects.all().delete()

    # حذف البروفايلات
    Profile.objects.all().delete()

    # حذف التوكينز
    from rest_framework.authtoken.models import Token
    Token.objects.all().delete()

    # حذف المستخدمين
    User.objects.exclude(is_superuser=True).delete()

    print("✅ All fake data deleted.")


def run():
    print("Generating fake data...")
    data = create_users_and_profiles()
    courses = create_courses(data["instructors"])
    register_students_and_assistants(courses, data["students"], data["assistants"])
    create_course_materials(courses)
    assignments = create_assignments(courses)
    create_solutions_and_grades(assignments, data["students"])
    create_chats_and_messages(User.objects.all())
    print("✅ Fake data generation completed.")


# python manage.py shell

# from scripts.populate_data import run, clear_data

# # لحذف كل البيانات الوهمية
# clear_data()

# # لإعادة توليدها
# run()

