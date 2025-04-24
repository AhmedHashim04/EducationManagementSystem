from django.core.exceptions import PermissionDenied
from django.views.generic import DeleteView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from account.permessions import  IsStudent, IsInstructor 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Course, CourseRegistration
from .serializers import CourseListSerializer, CourseDetailsSerializer
from django.shortcuts import get_object_or_404

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    # authentication_classes = [JWTAuthentication]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsStudent | IsInstructor]

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profile', None)
        if user_profile:
            if user_profile.role == 'student':
                return Course.objects.exclude(registrations__student=user_profile)
            elif user_profile.role == 'instructor':
                return Course.objects.exclude(instructor=user_profile)
        return Course.objects.all()

    def _validate_student_enrollment(self, student, course):
        if student.role != 'student':
            raise PermissionDenied('Only students can enroll/unenroll in courses')

    def _get_course_and_validate(self, course_code, check_exists=False):
        course = get_object_or_404(Course, code=course_code)
        student = self.request.user.profile
        self._validate_student_enrollment(student, course)
        
        registration_exists = CourseRegistration.objects.filter(
            student=student, 
            course=course
        ).exists()

        if check_exists and not registration_exists:
            raise PermissionDenied('Student is not enrolled in this course')
        elif not check_exists and registration_exists:
            raise PermissionDenied('Student already enrolled in this course')

        return course, student

    def post(self, request, *args, **kwargs):
        """Handle course enrollment"""
        course_code = request.data.get('code')
        course, student = self._get_course_and_validate(course_code)

        if not course.is_active:
            return Response({'error': 'Course is not active'}, status=400)

        CourseRegistration.objects.create(
            student=student, 
            course=course, 
            status='accepted'
        )
        return Response({'message': 'Student enrolled successfully'}, status=200)



class MyCourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer

    # authentication_classes = [JWTAuthentication]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsStudent | IsInstructor]


    def _validate_student_enrollment(self, student, course):
        if student.role != 'student':
            raise PermissionDenied('Only students can enroll/unenroll in courses')

    def _get_course_and_validate(self, course_code, check_exists=False):
        course = get_object_or_404(Course, code=course_code)
        student = self.request.user.profile
        self._validate_student_enrollment(student, course)
        
        registration_exists = CourseRegistration.objects.filter(
            student=student, 
            course=course
        ).exists()

        if check_exists and not registration_exists:
            raise PermissionDenied('Student is not enrolled in this course')
        elif not check_exists and registration_exists:
            raise PermissionDenied('Student already enrolled in this course')

        return course, student

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profile', None)

        if user_profile.role == 'student':
            return Course.objects.filter(registrations__student=user_profile)
        elif user_profile.role == 'instructor':
            return Course.objects.filter(instructor=user_profile)

        return Course.objects.none()

class CourseDetails(generics.RetrieveDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailsSerializer
    lookup_field = 'code'
    lookup_url_kwarg = 'courseCode'

    # authentication_classes = [JWTAuthentication]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsStudent | IsInstructor]

    def is_enrolled(self, course):
        student_id = self.request.user.profile
        return CourseRegistration.objects.filter(student=student_id, course=course).exists()
    
    def is_instructor(self, course):
        instructor_id = self.request.user.profile
        return instructor_id == course.instructor
    
    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()
        print(course)
        
        if not (self.is_enrolled(course) or self.is_instructor(course)):
            return Response(
                {'error': 'Only students/instructor in course can view course details'},
                status=403
            )

        serializer = self.get_serializer(course)
        return Response({
            'course': serializer.data,
        })

    def delete(self, request, *args, **kwargs):
        """Handle course unenrollment"""
        course = self.get_object()
        student = request.user.profile
    
        # Validate student can unenroll
        if student.role != 'student':
            raise PermissionDenied('Only students can unenroll from courses')

        # Check if student is enrolled and delete in one query
        deleted, _ = CourseRegistration.objects.filter(
            student=student,
            course=course
        ).delete()

        if not deleted:
            raise PermissionDenied('Student is not enrolled in this course')

        return Response({'message': 'Student unenrolled successfully'}, status=200)


#If you want use swagger on APIView write this over get()
    # @swagger_auto_schema(
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'my_courses', openapi.IN_QUERY, description="Get User_Courses", type=openapi.TYPE_BOOLEAN
    #         ),
    #     ]
    # )
#else use this on get() override in generics

# class CourseListView(generics.ListCreateAPIView):   
#     serializer_class = CourseListSerializer
    # authentication_classes = [JWTAuthentication]
#     authentication_classes = [BasicAuthentication]
#     # permission_classes = [IsStudent | IsInstructor]
#     permission_classes = [IsAuthenticated]

#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter(
#                 'my_courses', openapi.IN_QUERY, description="Get User_Courses", type=openapi.TYPE_BOOLEAN
#             ),
#         ]
#     )
#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)

#     def get_queryset(self):
#         user_profile = getattr(self.request.user, 'profile', None)
#         if not user_profile:
#             return Course.objects.none()

#         # we will handle the my_courses query parameter here 
#         show_my_courses = self.request.query_params.get('my_courses', 'false').lower() == 'true'

#         if show_my_courses:
#             if user_profile.role == 'student':
#                 return Course.objects.filter(registrations__student=user_profile)
#             elif user_profile.role == 'instructor':
#                 return Course.objects.filter(instructor=user_profile)
#         else:
#             if user_profile.role == 'student':
#                 return Course.objects.exclude(registrations__student=user_profile)
#             elif user_profile.role == 'instructor':
#                 return Course.objects.exclude(instructor=user_profile)
        
#         return Course.objects.none() # This works because none() returns a QuerySet
#         """
#         - Type Consistency :
#             - Course.objects.none() returns an empty QuerySet
#             - This maintains the same type as other get_queryset() returns
#             - Your code can chain filters or annotations without type checking
#         - Performance :
#             - none() is optimized to not hit the database
#             - Returns an empty queryset immediately
#         - Compatibility :
#         # Bad approaches:
#             return None  # Will raise TypeError when DRF tries to serialize
#             return []    # Not a QuerySet, breaks Django's ORM chain
#             return Response(error=...)  # Wrong place for response, breaks DRF view flow
#         """

