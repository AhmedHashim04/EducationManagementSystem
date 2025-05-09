from django.db import models
from account.models import Profile
from course.models import Course
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

class Assignment(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Solution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student    = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    content   = models.TextField()
    file_attachment = models.FileField(upload_to='solutions/', blank=True, null=True)
    class Meta:
        verbose_name = "Solution"
        verbose_name_plural = "Solutions"
        ordering = ['assignment', 'student']

    def __str__(self):
        student_name = f"{self.student.user.first_name} {self.student.user.last_name}" if self.student and self.student.user else "Unknown"
        return f'{student_name} - {self.assignment.title} '


class Grade(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    solution   = models.OneToOneField(Solution, on_delete=models.CASCADE)
    score      = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    feedback    = models.TextField(blank=True, null=True)
    graded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        ordering = ['solution', 'graded_at']

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

    def save(self, *args, **kwargs):
        if not self.slug:
            student_name = self.get_student_name()
            assignment_title = self.get_assignment_title()
            self.slug = slugify(f"{assignment_title}-{student_name}")
        super().save(*args, **kwargs)