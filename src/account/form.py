from django.contrib.auth.forms import UserCreationForm
from .models import User

# from django import forms
# class RegisterForm(forms.Form):
#     class Meta:
#         model = Profile
#         fields = "_all_"



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2','email']
