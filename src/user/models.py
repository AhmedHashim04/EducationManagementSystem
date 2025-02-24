from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

# from pycountry import countries

# def get_country():
#     return [(country.name,country.alpha_2) for country in countries]
# Create your models here.



class Profile(models.Model):

    ROLES = (
        ('manager','Manager'),
        ('instructor','Instructor'),
        ('student','Student')
    )

    STATUS = (

        ('banned','Banned'),
        ('active','Active')
    ) 

    user = models.OneToOneField(User, verbose_name=_("User"), on_delete=models.CASCADE)
    role = models.CharField(choices  = ROLES , verbose_name=_("Role"), max_length=50)
    status = models.CharField(choices  = STATUS , verbose_name=_("Status"), max_length=50)
    

    def __str__(self):
        return f'Dr {self.user.first_name}  {self.user.first_name}' if self.role == 'instructor' \
          else f'   {self.user.first_name}  {self.user.first_name}'


