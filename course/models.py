from django.db import models
from django.utils.translation import gettext as _
from account.models import Profile
# Create your models here.

class Course(models.Model):
    code = models.CharField(_("Code"), max_length=50,unique=True)
    name = models.CharField(_("Name"), max_length=50)
    description = models.TextField(_("Description"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    instructor = models.ForeignKey(Profile, verbose_name=_("Instructor"), on_delete=models.CASCADE, related_name='courses', limit_choices_to={'role': 'instructor'})
    registration_end_at = models.DateTimeField(_("Registration End At"), null=True, blank=True)

    def __str__(self):
        instructor_name = f"{self.instructor.user.first_name} {self.instructor.user.last_name}" if self.instructor and self.instructor.user else "Unknown"
        return f'{self.code} - {self.name} - Dr: {instructor_name}'
    
class CourseRegistration(models.Model):
    student = models.ForeignKey(Profile, verbose_name=_("Student"), on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='registrations')
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='registrations')
    register_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        student_name = f"{self.student.user.first_name} {self.student.user.last_name}" if self.student and self.student.user else "Unknown"
        return f'{student_name} in {self.course.name}'

class CourseAssistant(models.Model):
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='assistants')
    assistant = models.ForeignKey(Profile, verbose_name=_("Assistant"), on_delete=models.CASCADE, limit_choices_to={'role': 'assistant'}, related_name='assistant_courses')
    register_at = models.DateTimeField(auto_now_add=True)
    permession = models.BooleanField(default=False)


    def __str__(self):
        student_name = f"{self.assistant.user.first_name} {self.assistant.user.last_name}" if self.assistant and self.assistant.user else "Unknown"
        return f'{student_name} in {self.course.name}'

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"), blank=True, null=True)
    file = models.FileField(_("File"), upload_to='course_materials/')
    uploaded_at = models.DateTimeField(_("Uploaded At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}"

    class Meta:
        verbose_name = _("Course Material")
        verbose_name_plural = _("Course Materials")
