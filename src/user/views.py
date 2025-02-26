from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .form import RegisterForm
# Create your views here.


def instructorRegistration(request):
    if request.method == 'POST' :

        newUser_form = RegisterForm(request.POST)

        if newUser_form.is_valid() :

            newUser_form.save(commit=False)
            newUser_form.is_active = False
            newUser_form.save()

            return JsonResponse({'message':'User created successfully','data':
                                 ({'username':newUser_form.cleaned_data.get('username')} ,
                                 {'activity':newUser_form.cleaned_data.get('is_active')}, 
                                 {'password':newUser_form.cleaned_data.get('password')} )
                                 
                                 })
            
    else :
        newUser_form = RegisterForm()
        
    return JsonResponse({'message':newUser_form})




def studentRegistration(request):
    pass
