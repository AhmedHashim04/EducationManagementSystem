
from django.contrib import admin
from django.urls import path
from .views import CourseList, CourseDetails

app_name = 'course'

urlpatterns = [
    path('allcourses/',CourseList.as_view(),name='courseList'),
    path('<int:id>',CourseDetails.as_view(),name='courseDetails'),
    

]


