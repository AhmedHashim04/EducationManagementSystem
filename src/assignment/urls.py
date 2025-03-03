
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from .views import AssignmentViewSet 
from django.urls import include

app_name = 'assignment'

router = routers.DefaultRouter()
router.register('assignments', AssignmentViewSet)

urlpatterns = [
	path('', include(router.urls)),
]


