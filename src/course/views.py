from django.shortcuts import render
from rest_framework.views import APIView
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


class CourseDetails(APIView):


    def get(self, request,id):
        course = Course.objects.get(pk = id)
        jsonCourses = CourseDetailsSerializer(course).data
        return Response(jsonCourses) 
    
    def put(self, request,id):
        course = Course.objects.get(pk = id)
        serialEditCourse = CourseDetailsSerializer(course, data=request.data)
        if serialEditCourse.is_valid():
            serialEditCourse.save()
            return Response(serialEditCourse.data, status=status.HTTP_201_CREATED)
        return Response(serialEditCourse.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,id):
        course = Course.objects.get(pk = id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)