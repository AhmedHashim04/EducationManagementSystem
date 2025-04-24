
from django.contrib import admin
from django.urls import path
from .views import CourseListView, CourseDetailView, MyCourseListView

app_name = 'course'

urlpatterns = [
    path('',CourseListView.as_view(),name='courseList'),
    path('me/',MyCourseListView.as_view(),name='myCourseList'),
    path('me/<str:course_code>/',CourseDetailView.as_view(),name='courseDetails'),

]


