
from django.contrib import admin
from django.urls import path
from .views import instructorRegistration
app_name = 'user'

urlpatterns = [
    path('register/',instructorRegistration,name='register'),
    

]


