
class Course(models.Model):
    code = models.CharField(_("Code"), max_length=50,unique=True)
    name = models.CharField(_("Name"), max_length=50)
    description = models.TextField(_("Description"))
    credit = models.FloatField(_("Credit"), null=True, blank=True, default=0)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    manager = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='managed_courses')
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    instructor = models.ForeignKey(Profile, verbose_name=_("Instructor"), on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        instructor_name = f"{self.instructor.user.first_name} {self.instructor.user.last_name}" if self.instructor and self.instructor.user else "Unknown"
        return f'{self.code} - {self.name} - Dr: {instructor_name}'
    
class CourseRegistration(models.Model):
    student = models.ForeignKey(Profile, verbose_name=_("Student"), on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='registrations')
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=10, default='pending', choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    register_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        student_name = f"{self.student.user.first_name} {self.student.user.last_name}" if self.student and self.student.user else "Unknown"
        return f'{student_name} in {self.course.name}'
from django.db import models
from account.models import Profile
from course.models import Course
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class Assignment(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()

    class Meta:
        verbose_name = "Assignment"
        verbose_name_plural = "Assignments"
        ordering = ['due_date']

    def __str__(self):
        return f'{self.pk} - {self.title} - {self.course.name}'


class Solution(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student    = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    sloution   = models.TextField()


    class Meta:
        verbose_name = "Solution"
        verbose_name_plural = "Solutions"
        ordering = ['assignment', 'student']

    def __str__(self):
        student_name = f"{self.student.user.first_name} {self.student.user.last_name}" if self.student and self.student.user else "Unknown"
        return f'{student_name} - {self.assignment.title} '


class Grade(models.Model):
    solution   = models.OneToOneField(Solution, on_delete=models.CASCADE)
    grade      = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    comment    = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        ordering = ['solution', 'created_at']

    def __str__(self):
        student_name = f"{self.solution.student.user.first_name} {self.solution.student.user.last_name}" if self.solution.student and self.solution.student.user else "Unknown"
        return f'{student_name} - {self.solution.assignment.title} - {self.grade}'

    def get_student_name(self):
        if self.solution.student and self.solution.student.user:
            return f"{self.solution.student.user.first_name} {self.solution.student.user.last_name}"
        return "Unknown"

    def get_assignment_title(self):
        return self.solution.assignment.title if self.solution.assignment else "Unknown"

    def get_grade(self):
        return self.grade if self.grade else 0

    def get_comment(self):
        return self.comment if self.comment else "No comment"

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings


 


# from pycountry import countries

# def get_country():
#     return [(country.name,country.alpha_2) for country in countries]
# Create your models here.



class Profile(models.Model):

    ROLES = (
        ('instructor','Instructor'),
        # ('assistant','Assistant'),
        ('student','Student')
    )

    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE,related_name="profile")

    role = models.CharField(choices  = ROLES , verbose_name=_("Role"), max_length=50)
    

    def __str__(self):
        return f'Dr {self.user} {self.user.first_name}  {self.user.first_name}' if self.role == 'instructor' \
        else f'Student {self.user} {self.user.first_name}  {self.user.first_name}'

        
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not Profile.objects.filter(user=instance).exists():
        # Get role from instance's temporary attribute or default to 'student'
        role = getattr(instance, '_role', 'student')
        Profile.objects.create(user=instance, role=role)
        Token.objects.create(user=instance)
    else:
        profile = Profile.objects.get(user=instance)
        token = Token.objects.get(user=instance)
        profile.save()
        token.save()


