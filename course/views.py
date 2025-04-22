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

"""
 1. Keep them separate (CourseList , MyCoursesList , and CourseDetails) Pros:
- Each view has a single responsibility
- Code is more maintainable
- Follows REST principles better
- Clearer API endpoints
2. Merge CourseList and MyCoursesList This could make sense because:
- Both handle course listing
- They share similar authentication and permissions
- Could be handled with a query parameter
 3. Keep CourseDetails Separate CourseDetails should remain separate because:
- It handles individual course details
- Has different lookup logic
- Different serializer
- Different access control logic
The best practice here would be to:

1. Merge CourseList and MyCoursesList into a single view with query parameter control
2. Keep CourseDetails separate
This gives you:

- /api/courses/?my_courses=true|false for listing courses
- /api/courses/<code>/ for course details
This approach:

- Reduces code duplication
- Maintains clear separation of concerns
- Follows REST principles
- Makes the API more intuitive
- Easier to maintain and extend
 """

# class CourseList(generics.ListCreateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseListSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsStudent | IsInstructor]

#     def get_queryset(self):
#         user_profile = getattr(self.request.user, 'profile', None)
#         if user_profile:
#             if user_profile.role == 'student':
#                 return Course.objects.exclude(registrations__student=user_profile)
#             elif user_profile.role == 'instructor':
#                 return Course.objects.exclude(instructor=user_profile)
#         return Course.objects.all()

#     def _validate_student_enrollment(self, student, course):
#         if student.role != 'student':
#             raise PermissionDenied('Only students can enroll/unenroll in courses')

#     def _get_course_and_validate(self, course_code, check_exists=False):
#         course = get_object_or_404(Course, code=course_code)
#         student = self.request.user.profile
#         self._validate_student_enrollment(student, course)
        
#         registration_exists = CourseRegistration.objects.filter(
#             student=student, 
#             course=course
#         ).exists()

#         if check_exists and not registration_exists:
#             raise PermissionDenied('Student is not enrolled in this course')
#         elif not check_exists and registration_exists:
#             raise PermissionDenied('Student already enrolled in this course')

#         return course, student

#     def post(self, request, *args, **kwargs):
#         """Handle course enrollment"""
#         course_code = request.data.get('course_code')
#         course, student = self._get_course_and_validate(course_code)

#         if not course.is_active:
#             return Response({'error': 'Course is not active'}, status=400)

#         CourseRegistration.objects.create(
#             student=student, 
#             course=course, 
#             status='accepted'
#         )
#         return Response({'message': 'Student enrolled successfully'}, status=200)

#     def delete(self, request, *args, **kwargs):
#         """Handle course unenrollment"""
#         course_code = request.data.get('course_code')
#         course, student = self._get_course_and_validate(course_code, check_exists=True)

#         CourseRegistration.objects.filter(
#             student=student, 
#             course=course
#         ).delete()
#         return Response({'message': 'Student unenrolled successfully'}, status=200)

# class MyCoursesList(generics.ListAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseListSerializer

#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsStudent | IsInstructor]

#     def get_queryset(self):
#         user_profile = getattr(self.request.user, 'profile', None)

#         if user_profile.role == 'student':
#             return Course.objects.filter(registrations__student=user_profile)
#         elif user_profile.role == 'instructor':
#             return Course.objects.filter(instructor=user_profile)

#         return Course.objects.none()

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

class CourseListView(generics.ListCreateAPIView):
    serializer_class = CourseListSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent | IsInstructor]

    def get_queryset(self):
        user_profile = getattr(self.request.user, 'profile', None)
        if not user_profile:
            return Course.objects.none()

        # we will handle the my_courses query parameter here 
        show_my_courses = self.request.query_params.get('my_courses', 'false').lower() == 'true'

        if show_my_courses:
            if user_profile.role == 'student':
                return Course.objects.filter(registrations__student=user_profile)
            elif user_profile.role == 'instructor':
                return Course.objects.filter(instructor=user_profile)
        else:
            if user_profile.role == 'student':
                return Course.objects.exclude(registrations__student=user_profile)
            elif user_profile.role == 'instructor':
                return Course.objects.exclude(instructor=user_profile)
        
        return Course.objects.none() # This works because none() returns a QuerySet
        """
        - Type Consistency :
            - Course.objects.none() returns an empty QuerySet
            - This maintains the same type as other get_queryset() returns
            - Your code can chain filters or annotations without type checking
        - Performance :
            - none() is optimized to not hit the database
            - Returns an empty queryset immediately
        - Compatibility :
        # Bad approaches:
            return None  # Will raise TypeError when DRF tries to serialize
            return []    # Not a QuerySet, breaks Django's ORM chain
            return Response(error=...)  # Wrong place for response, breaks DRF view flow
        """

