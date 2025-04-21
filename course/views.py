from django.core.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.response import Response
from account.permessions import  IsStudent, IsInstructor 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from .models import Course, CourseRegistration
from account.models import Profile
from .serializers import CourseListSerializer, CourseDetailsSerializer



class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent | IsInstructor]

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profile', None)
        if user_profile:
        
            if user_profile.role == 'student':
                return Course.objects.exclude(registrations__student=user_profile)

            elif user_profile.role == 'instructor':
                return Course.objects.exclude(instructor=user_profile)

        return Course.objects.all()

class MyCoursesList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent | IsInstructor]

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profile', None)

        if user_profile.role == 'student':
            return Course.objects.filter(registrations__student=user_profile)
        elif user_profile.role == 'instructor':
            return Course.objects.filter(instructor=user_profile)

        return Course.objects.none()

class CourseDetails(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailsSerializer
    lookup_field = 'code'
    lookup_url_kwarg = 'courseCode'

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent | IsInstructor]

    def is_enrolled(self, course):
        student_id = self.request.user.profile
        return CourseRegistration.objects.filter(student=student_id, course=course).exists()
    
    def is_instructor(self, course):
        instructor_id = self.request.user.profile
        return Course.objects.filter(instructor=instructor_id, code=course.code).exists()
    
    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()
        
        if not (self.is_enrolled(course) or self.is_instructor(course)):
            return Response(
                {'error': 'Only students/instructor in course can view course details'},
                status=403
            )

        serializer = self.get_serializer(course)

        return Response({
            'course': serializer.data,
        })




@authentication_classes([JWTAuthentication])
@api_view(['GET'])
def enroll_student(request, course_code):

    course = get_object_or_404(Course, code=course_code)
    student = request.user.profile

    if CourseRegistration.objects.filter(student=student, course=course).exists():
        return Response({'error': 'Student already enrolled in this course'}, status=400)

    if not course.is_active:
        return Response({'error': 'Course is not active'}, status=400)

    CourseRegistration.objects.create(student=student, course=course, status='accepted')
    return Response({'message': 'Student enrolled successfully'}, status=200)


@authentication_classes([JWTAuthentication])
@api_view(['GET'])
def unenroll_student(request, course_code):

    student = request.user.profile
    course = get_object_or_404(Course, code=course_code)

    registration = CourseRegistration.objects.filter(student=student, course=course)
    if not registration.exists():
        return Response({'error': 'Student is not enrolled in this course'}, status=400)

    registration.delete()
    return Response({'message': 'Student unenrolled successfully'}, status=200)
