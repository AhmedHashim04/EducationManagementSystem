from django.db import models
from django.utils.translation import gettext as _
from account.models import Profile
# Create your models here.

class Course(models.Model):
    code = models.CharField(_("Code"), max_length=50)
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

