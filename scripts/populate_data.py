
from django.db import transaction
from django.utils.text import slugify
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

@transaction.atomic
def create_users_and_profiles():
    users_profiles = {"instructors": [], "assistants": [], "students": []}
    bulk_users = []
    for role, num in [("instructor", NUM_INSTRUCTORS), ("assistant", NUM_ASSISTANTS), ("student", NUM_STUDENTS)]:
        for _ in range(num):
            bulk_users.append(User(username=fake.user_name(), email=fake.email()))
    users = User.objects.bulk_create(bulk_users)

    bulk_profiles = []
    for i, user in enumerate(users):
        if i < NUM_INSTRUCTORS:
            role = 'instructor'
        elif i < NUM_INSTRUCTORS + NUM_ASSISTANTS:
            role = 'assistant'
        else:
            role = 'student'
        bulk_profiles.append(Profile(user=user, role=role))
        users_profiles[f"{role}s"].append(bulk_profiles[-1])

    Profile.objects.bulk_create(bulk_profiles)
    return users_profiles

@transaction.atomic
def create_courses(instructors):
    return Course.objects.bulk_create([
        Course(
            code=f"CSE{random.randint(100, 999)}",
            name=fake.catch_phrase(),
            description=fake.text(),
            instructor=random.choice(instructors),
            registration_start_at=timezone.now(),
            registration_end_at=timezone.now() + timezone.timedelta(days=30)
        )
        for _ in range(NUM_COURSES)
    ])

@transaction.atomic
def register_students_and_assistants(courses, students, assistants):
    registrations = []
    course_assistants = []
    for course in courses:
        registrations.extend([
            CourseRegistration(student=s, course=course)
            for s in random.sample(students, k=10)
        ])
        course_assistants.extend([
            CourseAssistant(course=course, assistant=a, permession=random.choice([True, False]))
            for a in random.sample(assistants, k=2)
        ])
    CourseRegistration.objects.bulk_create(registrations)
    CourseAssistant.objects.bulk_create(course_assistants)

@transaction.atomic
def create_course_materials(courses):
    materials = []
    for course in courses:
        for _ in range(2):
            materials.append(CourseMaterial(
                course=course,
                title=fake.sentence(),
                description=fake.text(),
                file='course_materials/sample.pdf',
                is_active=True
            ))
    CourseMaterial.objects.bulk_create(materials)

@transaction.atomic
def create_assignments(courses):
    assignments = []
    used_slugs = set()
    for course in courses:
        for _ in range(NUM_ASSIGNMENTS_PER_COURSE):
            title = fake.sentence(nb_words=4)
            base_slug = slugify(title)
            slug = base_slug
            counter = 1
            while slug in used_slugs:
                slug = f"{base_slug}-{counter}"
                counter += 1
            used_slugs.add(slug)
            assignments.append(Assignment(
                title=title,
                description=fake.paragraph(),
                course=course,
                due_date=timezone.now() + timezone.timedelta(days=random.randint(7, 30)),
                slug=slug
            ))
    return Assignment.objects.bulk_create(assignments)
@transaction.atomic
def create_solutions_and_grades(assignments, students):
    solutions = []
    grades = []
    for assignment in assignments:
        for student in random.sample(students, k=NUM_SOLUTIONS_PER_ASSIGNMENT):
            sol = Solution(
                assignment=assignment,
                student=student,
                content=fake.paragraph(),
                file_attachment=None
            )
            solutions.append(sol)

    Solution.objects.bulk_create(solutions)

    for sol in solutions:
        grades.append(Grade(
            solution=sol,
            score=random.randint(50, 100),
            feedback=fake.sentence()
        ))
    Grade.objects.bulk_create(grades)

@transaction.atomic
def create_chats_and_messages():
    users = list(User.objects.all())
    messages = []
    for _ in range(10):
        participants = random.sample(users, 2)
        chat = Chat.objects.create()
        chat.participants.set(participants)
        messages.extend([
            Message(
                chat=chat,
                sender=random.choice(participants),
                content=fake.sentence(),
                is_read=random.choice([True, False])
            )
            for _ in range(random.randint(3, 6))
        ])
    Message.objects.bulk_create(messages)

def run():
    print("🚀 Generating fake data...")
    with transaction.atomic():
        data = create_users_and_profiles()
        courses = create_courses(data["instructors"])
        register_students_and_assistants(courses, data["students"], data["assistants"])
        create_course_materials(courses)
        assignments = create_assignments(courses)
        create_solutions_and_grades(assignments, data["students"])
        create_chats_and_messages()
    print("✅ Fake data generation completed.")


def clear_data():
    print("⚠️  Deleting all fake data...")
    Message.objects.all().delete()
    Chat.objects.all().delete()
    Grade.objects.all().delete()
    Solution.objects.all().delete()
    Assignment.objects.all().delete()
    CourseMaterial.objects.all().delete()
    CourseRegistration.objects.all().delete()
    CourseAssistant.objects.all().delete()
    Course.objects.all().delete()
    Profile.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()
    print("✅ All fake data deleted.")



# python manage.py shell

# from scripts.populate_data import run, clear_data

# # لحذف كل البيانات الوهمية
# clear_data()

# # لإعادة توليدها
# run()

