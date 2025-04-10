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