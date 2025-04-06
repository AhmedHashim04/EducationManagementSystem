from django.contrib import admin
from django.urls import path
from .views import CreateAssignment, AssignmentDetailView ,SolveAssignment 

from django.conf import settings
from django.urls import include

app_name = 'assignment'

urlpatterns = [
    path('<str:course_code>/assignments/', CreateAssignment.as_view(), name='assignments'),
    path('<str:course_code>/assignments/<int:assignment_id>/', AssignmentDetailView.as_view(), name='assignment_detail'),
    path('<str:course_code>/assignments/<int:assignment_id>/solution', SolveAssignment.as_view(), name='assignment_solution'),

]
