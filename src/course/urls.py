
from django.contrib import admin
from django.urls import path
from .views import CourseList, CourseDetails ,enroll_student , unenroll_student ,MyCourseList

app_name = 'course'

urlpatterns = [
    path('',CourseList.as_view(),name='courseList'),
    path('my/',MyCourseList.as_view(),name='mycourseList'),
    path('my/<str:courseCode>/',CourseDetails.as_view(),name='courseDetails'),
    path('enroll_student/<str:course_code>/', enroll_student, name='enroll_student'),
    path('my/<str:courseCode>/unenroll_student/', unenroll_student, name='unenroll_student'),

]


