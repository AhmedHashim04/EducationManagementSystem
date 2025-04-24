from django.core.exceptions import PermissionDenied
from django.views.generic import DeleteView
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from account.permessions import IsStudent, IsInstructor 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BasicAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Course, CourseRegistration, CourseMaterial
from .serializers import CourseListSerializer, CourseDetailSerializer, CourseMaterialSerializer

from django.shortcuts import get_object_or_404

class CourseListView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
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

    @swagger_auto_schema(
        operation_id='list_unenrolled_courses',
        operation_description="Returns a list of courses that the authenticated user has not enrolled in yet",
        responses={
            200: openapi.Response(
                description="Success",
                schema=CourseListSerializer(many=True)
            ),
            401: openapi.Response(description="Authentication credentials were not provided"),
            403: openapi.Response(description="Permission denied")
        },
        tags=['courses']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id='enroll_course',
        operation_description="Enroll a student in a course",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['code'],
            properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING, description='Course code')
            }
        ),
        responses={
            200: openapi.Response(
                description="Successfully enrolled",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: openapi.Response(
                description="Bad request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Course not found")
        },
        tags=['courses']
    )
    def post(self, request, *args, **kwargs):
        course_code = request.data.get('code')
        course, student = self._get_course_and_validate(course_code)

        if not course.is_active:
            return Response(
                {'error': 'Course is not active'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        CourseRegistration.objects.create(
            student=student, 
            course=course, 
            status='accepted'
        )
        return Response(
            {'message': 'Student enrolled successfully'}, 
            status=status.HTTP_200_OK
        )

class MyCourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsStudent | IsInstructor]

    @swagger_auto_schema(operation_id='list_enrolled_courses',operation_description="Returns a list of courses associated with the authenticated user",
    responses={200: openapi.Response
            (
                description="Success",
                schema=CourseListSerializer(many=True)
                                                        ),
            401: openapi.Response(description="Authentication credentials were not provided"),
            403: openapi.Response(description="Permission denied")
        },
        tags=['courses']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profile', None)
        if user_profile.role == 'student':
            return Course.objects.filter(registrations__student=user_profile)
        elif user_profile.role == 'instructor':
            return Course.objects.filter(instructor=user_profile)
        return Course.objects.none()

class CourseDetailView(generics.RetrieveDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    lookup_field = 'code'
    lookup_url_kwarg = 'course_code'
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsStudent | IsInstructor]

    def is_enrolled(self, course):
        student_id = self.request.user.profile
        return CourseRegistration.objects.filter(student=student_id, course=course).exists()
    
    def is_instructor(self, course):
        instructor_id = self.request.user.profile
        return instructor_id == course.instructor

    @swagger_auto_schema(operation_id='get_course_details',operation_description="Retrieve details of a specific course",
        responses={
            200: openapi.Response

            (   description="Success",
                schema=CourseDetailSerializer()
                                                    ),
            401: openapi.Response(description="Authentication credentials were not provided"),
            403: openapi.Response(
                description="Permission denied",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            404: openapi.Response(description="Course not found")
        },
        tags=['courses']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()
        
        if not (self.is_enrolled(course) or self.is_instructor(course)):
            return Response(
                {'error': 'Only students/instructor in course can view course details'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(course)
        return Response({
            'course': serializer.data,
        })

    @swagger_auto_schema(
        operation_id='unenroll_course',
        operation_description="Unenroll a student from a course",
        responses={
            200: openapi.Response(
                description="Successfully unenrolled",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            401: openapi.Response(description="Authentication credentials were not provided"),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Course not found")
        },
        tags=['courses']
    )
    def delete(self, request, *args, **kwargs):
        course = self.get_object()
        student = request.user.profile
    
        if student.role != 'student':
            raise PermissionDenied('Only students can unenroll from courses')

        deleted, _ = CourseRegistration.objects.filter(
            student=student,
            course=course
        ).delete()

        if not deleted:
            raise PermissionDenied('Student is not enrolled in this course')

        return Response(
            {'message': 'Student unenrolled successfully'}, 
            status=status.HTTP_200_OK
        )
class CourseMaterialView(generics.ListCreateAPIView):
    serializer_class = CourseMaterialSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsStudent | IsInstructor]
    
    def get_queryset(self):
        course_code = self.kwargs.get('course_code')
        course = get_object_or_404(Course, code=course_code)
        
        user_profile = self.request.user.profile
        
        # Check if student is enrolled or is the course instructor
        if user_profile.role == 'student':
            if not CourseRegistration.objects.filter(
                student=user_profile, 
                course=course
            ).exists():
                raise PermissionDenied('Only enrolled students can access course materials')
        elif user_profile.role == 'instructor' and course.instructor != user_profile:
            raise PermissionDenied('Only course instructor can access course materials')
            
        # Return active materials for the course
        return CourseMaterial.objects.filter(course=course, is_active=True)

    def perform_create(self, serializer):
        course_code = self.kwargs.get('course_code')
        course = get_object_or_404(Course, code=course_code)
        
        # Verify instructor permissions
        if self.request.user.profile.role != 'instructor' or course.instructor != self.request.user.profile:
            raise PermissionDenied('Only course instructor can add materials')

        serializer.save(course=course)

    @swagger_auto_schema(
        operation_id='list_course_materials',
        operation_description="Get all materials for a specific course",
        responses={
            200: CourseMaterialSerializer(many=True),
            401: openapi.Response(description="Authentication credentials were not provided"),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Course not found")
        },
        tags=['course-materials']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id='create_course_material',
        operation_description="Add new material to a course",
        request_body=CourseMaterialSerializer,
        responses={
            201: CourseMaterialSerializer,
            400: openapi.Response(description="Invalid input"),
            401: openapi.Response(description="Authentication credentials were not provided"),
            403: openapi.Response(description="Permission denied"),
            404: openapi.Response(description="Course not found")
        },
        tags=['course-materials']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
