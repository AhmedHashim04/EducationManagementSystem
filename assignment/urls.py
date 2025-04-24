from django.urls import path
from .views import (
    AssignmentListCreateView,
    AssignmentDetailView,
    AssignmentSolutionView,
    AssignmentGradeListView,
)

app_name = 'assignment'

urlpatterns = [
    path('<str:course_code>/assignments/',AssignmentListCreateView.as_view(),name='assignments'),
    path('<str:course_code>/assignments/<slug:assignment_slug>/',AssignmentDetailView.as_view(),name='assignment_detail'),
    path('<str:course_code>/assignments/<slug:assignment_slug>/solution/', AssignmentSolutionView.as_view(),name='assignment_solution'),
    path('<str:course_code>/assignments/<slug:assignment_slug>/solution/<int:solution_id>/grade/',AssignmentGradeListView.as_view(),name='assignment_grade'),
]
