from django.shortcuts import render
from .models import Assignment, Grade
from rest_framework import generics
from .serializer import CourseAssignmentsSerializer , AssignmentSerializer

# Create your views here.

# for Course Instructor
class CourseAssignments(generics.ListCreateAPIView):
    serializer_class = CourseAssignmentsSerializer

    def get_queryset(self):
        course_id = self.kwargs['course_code']
        return Assignment.objects.filter(course__code=course_id)

class CertainAssignment(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssignmentSerializer
    lookup_field = 'id' 
    def get_queryset(self):
        slug = self.kwargs['id']
        course_id = self.kwargs['course_code']
        return Assignment.objects.filter(course__code=course_id, id=slug)
