from django.db import models
from user.models import Profile
from course.models import Course
import uuid

class Assignment(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()

    def __str__(self):
        return self.title + ' - ' + self.course.name


class Grade(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student    = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    sloution   = models.TextField()
    grade      = models.DecimalField(max_digits=5, decimal_places=2 ,default=-1)

    def __str__(self):
        return f'{self.student.user.first_name} - {self.assignment.title} - {self.grade}'
    