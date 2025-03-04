from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status 

from assignment.models import Assignment
from assignment.serializer import CourseAssignmentsSerializer

from .models import Course, CourseRegistration
from .serializer import CourseSerializer, CourseDetailsSerializer


#Instructor View
class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



class CourseDetails(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailsSerializer
    lookup_field = 'code'
    lookup_url_kwarg = 'courseCode'
    
    def get(self, request, *args, **kwargs):
        course = self.get_object()
        assignments = Assignment.objects.filter(course=course).values_list('title', flat=True)
        serializer = self.get_serializer(course)
        return Response({'course': serializer.data, 'assignments': list(assignments)})
    
    

    
class CourseCreate(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



