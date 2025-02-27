from django.db import models
from django.utils.translation import gettext as _
from user.models import Profile
# Create your models here.

class Course(models.Model):
    code = models.CharField(_("Code"), max_length=50)
    name = models.CharField(_("Name"), max_length=50)
    description = models.TextField(_("Description"))
    credit = models.FloatField(_("Credit"),null=True, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    manager = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='managed_courses')
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    instructor = models.ForeignKey(Profile, verbose_name=_("Instructor"), on_delete=models.CASCADE, related_name='courses')
    # chaphters = models.ManyToManyField('Chapter', verbose_name=_("Chapters"), related_name='courses')


    def __str__(self):
        return f'{self.code} - {self.name} - Dr : {self.Instructor.user.first_name} {self.Instructor.user.last_name}'
    
class CourseRegistration(models.Model):
    student_id = models.ForeignKey(Profile, verbose_name=_("Student"), on_delete=models.CASCADE,limit_choices_to='student' ,related_name='registrations')
    course_id = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=10, default='pending', choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    register_at = models.DateTimeField(auto_now_add=True)
    # accepted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.student_id.user.first_name} {self.student_id.user.last_name} in {self.course_id.name}'
