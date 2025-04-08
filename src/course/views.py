from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view 
from django.shortcuts import get_object_or_404

from assignment.models import Assignment
from assignment.serializer import CourseAssignmentsSerializer

from .models import Course, CourseRegistration
from .serializer import CourseSerializer, CourseDetailsSerializer


    
class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.profile.role == 'student':
            student_id = self.request.user.profile
            courses = Course.objects.exclude(registrations__student_id=student_id)
            return courses
         
        elif self.request.user.profile.role == 'instructor':
            instructor_id = self.request.user.profile
            courses = Course.objects.exclude(instructor=instructor_id)
            return courses
        
        return super().get_object()



class MyCourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        if self.request.user.profile.role == 'student':
            student_id = self.request.user.profile
            courses = Course.objects.filter(registrations__student_id=student_id)
            return courses
         
        elif self.request.user.profile.role == 'instructor':
            instructor_id = self.request.user.profile
            courses = Course.objects.filter(instructor=instructor_id)
            return courses
        
        return super().get_object()

class CourseDetails(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailsSerializer
    lookup_field = 'code'
    lookup_url_kwarg = 'courseCode'

    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()

        user_profile = request.user.profile

        is_enrolled = CourseRegistration.objects.filter(
            student_id=user_profile, course_id=course.id
        ).exists()

        is_instructor = course.instructor == user_profile

        if not (is_enrolled or is_instructor):
            return Response(
                {'error': 'Only students/instructor in course can view course details'},
                status=403
            )

        assignments = Assignment.objects.filter(course=course).values_list('title', flat=True)
        serializer = self.get_serializer(course)

        return Response({
            'course': serializer.data,
            'assignments': list(assignments)
        })

def is_student(request):
    if request.user.profile.role != 'student':
        raise PermissionDenied('Only students can enroll or unenroll in courses')

def get_course(course_code):
    return get_object_or_404(Course, code=course_code)

@api_view(['GET'])
def enroll_student(request, course_code):
    is_student(request)

    student_id = request.user.profile
    course = get_course(course_code)

    if CourseRegistration.objects.filter(student_id=student_id, course_id=course).exists():
        return Response({'error': 'Student already enrolled in this course'}, status=400)

    if not course.is_active:
        return Response({'error': 'Course is not active'}, status=400)

    CourseRegistration.objects.create(student_id=student_id, course_id=course, status='accepted')
    return Response({'message': 'Student enrolled successfully'}, status=200)

@api_view(['GET'])
def unenroll_student(request, course_code):

    is_student(request)

    student_id = request.user.profile
    course = get_course(course_code)

    if not CourseRegistration.objects.filter(student_id=student_id, course_id=course).exists():
        return Response({'error': 'Student is not enrolled in this course'}, status=400)

    CourseRegistration.objects.filter(student_id=student_id, course_id=course).delete()
    return Response({'message': 'Student unenrolled successfully'}, status=200)
