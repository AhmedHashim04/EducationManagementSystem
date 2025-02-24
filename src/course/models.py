from django.db import models
from django.models.auth import User
from pycountry import countries
# Create your models here.

def get_country():
    return [(country.name,country.alpha_2) for country in countries]

class UserRole(models.Model):
    role_name = models.CharField(max_length=50,choices=(('Admin','Admin'),('Instructor','Instructor'),('Student','Student')))
    def __str__(self):
        return self.role_name

class UserProfile(User):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_role = models.OneToOneField(UserRole, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='images/', default='images/default.jpg')
    user_phone = models.CharField(max_length=50)
    user_address = models.CharField(max_length=50)
    user_country = models.CharField(max_length=50)
    user_created_at = models.DateTimeField(auto_now_add=True)
    user_updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username


class StudentProfile(UserProfile):
    student_courses = models.ManyToManyField('Course', related_name='student_courses')
    student_enrolled_at = models.DateTimeField()
    

class InstructorProfile(UserProfile):
    instructor_courses = models.ManyToManyField('Course', related_name='instructor_courses')
    instructor_joined_at = models.DateTimeField()
