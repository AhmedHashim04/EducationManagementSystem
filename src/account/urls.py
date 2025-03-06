
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

# from .views import instructorRegistration
app_name = 'account'

urlpatterns = [
    # path('register/',instructorRegistration,name='register'),
    path('auth_token/',obtain_auth_token,name='getToken'),


    

]


