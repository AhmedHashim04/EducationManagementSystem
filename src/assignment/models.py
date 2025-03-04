from django.db import models
from user.models import Profile
from course.models import Course


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()

    def _str_(self):
        return self.title


class Grade(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student    = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    sloution   = models.TextField()
    grade      = models.DecimalField(max_digits=5, decimal_places=2)

    def _str_(self):
        return f'{self.student.name} - {self.assignment.title} - {self.grade}'
    