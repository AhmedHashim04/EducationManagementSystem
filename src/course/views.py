from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status 

from .models import Course, CourseRegistration
from .serializer import CourseSerializer, CourseDetailsSerializer

class CourseList(APIView):

    def get(self, request):
        courses = Course.objects.all()
        jsonCourses = CourseSerializer(courses, many=True).data
        return Response(jsonCourses)
    
    def post(self, request):
        serialNewCourse = CourseSerializer(data=request.data)
        if serialNewCourse.is_valid():
            serialNewCourse.save()
            return Response(serialNewCourse.data, status=status.HTTP_201_CREATED)
        return Response(serialNewCourse.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailsSerializer
    lookup_field = 'id'

    
class CourseCreate(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer