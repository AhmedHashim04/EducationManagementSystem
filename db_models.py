from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
import uuid
from account.models import Profile
from course.models import Course
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
class Profile(models.Model):
    ROLES = (('instructor','Instructor'),('assistant','Assistant'),('student','Student'))
    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE,related_name="profile")
    role = models.CharField(choices  = ROLES , verbose_name=_("Role"), max_length=50)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name=_("Avatar"))
    gpa = models.FloatField(_("GPA"), null=True, blank=True, default=0)
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not Profile.objects.filter(user=instance).exists():
        role = getattr(instance, '_role', 'student')
        Profile.objects.create(user=instance, role=role)
        Token.objects.create(user=instance)
    else:
        profile = Profile.objects.get(user=instance)
        token = Token.objects.get(user=instance)
        profile.save()
        token.save()
class Assignment(models.Model):
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    title = models.CharField(max_length=255, blank=False, null=False,unique=True,)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=False, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
class Solution(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='solutions')
    student    = models.ForeignKey(Profile, on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='solutions')
    content    = models.TextField()
    file_attachment = models.FileField(upload_to='solutions/', blank=True, null=True)
class Grade(models.Model):
    solution   = models.OneToOneField(Solution, on_delete=models.CASCADE, related_name='grade')
    score      = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    feedback    = models.TextField(blank=True, null=True)
    graded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    participants = models.ManyToManyField(User, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
class Course(models.Model):
    code = models.CharField(_("Code"), max_length=50,unique=True)
    name = models.CharField(_("Name"), max_length=50)
    description = models.TextField(_("Description"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    instructor = models.ForeignKey(Profile, verbose_name=_("Instructor"), on_delete=models.CASCADE, related_name='courses')
    registration_start_at = models.DateTimeField(_("Registration Start At"), null=True, blank=True)
    registration_end_at = models.DateTimeField(_("Registration End At"), null=True, blank=True)
class CourseRegistration(models.Model):
    student = models.ForeignKey(Profile, verbose_name=_("Student"), on_delete=models.CASCADE, limit_choices_to={'role': 'student'}, related_name='registrations')
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='registrations')
    register_at = models.DateTimeField(auto_now_add=True)
class CourseAssistant(models.Model):
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='assistants')
    assistant = models.ForeignKey(Profile, verbose_name=_("Assistant"), on_delete=models.CASCADE, limit_choices_to={'role': 'assistant'}, related_name='assistant_courses')
    register_at = models.DateTimeField(auto_now_add=True)
    permession = models.BooleanField(default=False)
class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, verbose_name=_("Course"), on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"), blank=True, null=True)
    file = models.FileField(_("File"), upload_to='course_materials/')
    uploaded_at = models.DateTimeField(_("Uploaded At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
