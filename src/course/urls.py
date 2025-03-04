
from django.contrib import admin
from django.urls import path
from .views import CourseList, CourseDetails, CourseCreate

app_name = 'course'

urlpatterns = [
    path('',CourseList.as_view(),name='courseList'),
    path('createcourse/',CourseCreate.as_view(),name='courseCreate'),
    path('<str:courseCode>/',CourseDetails.as_view(),name='courseDetails'),
    

]


