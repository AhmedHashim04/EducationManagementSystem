
from django.contrib import admin
from django.urls import path
from .views import AllCourseListView, CourseDetailView, MyCourseListView, CourseAssistantPermessionView, CourseMaterialView

app_name = 'course'

urlpatterns = [
    path('',AllCourseListView.as_view(),name='courseList'),
    path('me/',MyCourseListView.as_view(),name='myCourseList'),
    path('me/<str:course_code>/',CourseDetailView.as_view(),name='courseDetails'),
    path('me/<str:course_code>/permession/',CourseAssistantPermessionView.as_view(),name='givePermession'),
    path('me/<str:course_code>/materials/',CourseMaterialView.as_view(),name='courseMaterials'),
]


