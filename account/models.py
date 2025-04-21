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
        ('assistant','Assistant'),
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


