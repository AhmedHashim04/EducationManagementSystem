from django.contrib import admin
from django.urls import path
from .views import CourseAssignments, CertainAssignment
from django.urls import include

app_name = 'assignment'

urlpatterns = [
    path('<str:course_code>/', CourseAssignments.as_view(), name='assignments'),
    path('<str:course_code>/<int:id>/', CertainAssignment.as_view(), name='one_assignment'),
]


