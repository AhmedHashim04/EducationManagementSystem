
from django.contrib import admin
from django.urls import path
from .views import CourseListView, CourseDetails

app_name = 'course'

urlpatterns = [
    path('',CourseListView.as_view(),name='courseList'),
    path('my/<str:courseCode>/',CourseDetails.as_view(),name='courseDetails'),

]


