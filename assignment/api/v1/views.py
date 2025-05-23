from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from assignment.models import Assignment, Solution, Grade
from .serializers import (
    CourseAssignmentCreateSerializer,
    AssignmentSolutionSerializer,
    AssignmentSolutionUpdateSerializer,
    StudentSolutionListSerializer,
    AssignmentGradeListSerializer
)
from django_ratelimit.decorators import ratelimit


from course.models import Course, CourseRegistration
from account.permessions import IsStudent, IsInstructor
from rest_framework.authentication import BasicAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CourseAccessMixin:
    """Base mixin for course access control"""
    def is_student_registered(self, course):
        """Check if the current user is a student registered in the course."""
        return (
            self.request.user.profile.role == 'student' and
            CourseRegistration.objects.filter(
                student=self.request.user.profile,
                course=course
            ).exists()
        )
    
    def is_course_instructor(self, course):
        """Check if the current user is the instructor of the course."""
        return (
            self.request.user.profile.role == 'instructor' and 
            course.instructor == self.request.user.profile
        )

    def get_course(self):
        """Get course object from URL parameter."""
        course_code = self.kwargs['course_code']
        return get_object_or_404(Course, code=course_code)

class AssignmentListCreateView(CourseAccessMixin, generics.ListCreateAPIView):
    """
    API endpoint for listing and creating assignments
    """
    serializer_class = CourseAssignmentCreateSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsInstructor | IsStudent]

    @swagger_auto_schema(
        operation_description="Get list of assignments for a course",
        responses={
            200: CourseAssignmentCreateSerializer(many=True),
            403: "Access denied"
        }
    )
    def get_queryset(self):
        course = self.get_course()
        return Assignment.objects.filter(course=course)

    @swagger_auto_schema(
        operation_description="Create a new assignment",
        request_body=CourseAssignmentCreateSerializer,
        responses={
            201: CourseAssignmentCreateSerializer,
            403: "Only course instructor can create assignments"
        }
    )
    def create(self, request, *args, **kwargs):
        course = self.get_course()
        if not self.is_course_instructor(course):
            return Response(
                {"detail": "Only course instructor can create assignments."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(course=course)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="List all assignments in a course",
        responses={
            200: CourseAssignmentCreateSerializer(many=True),
            403: "Access denied"
        }
    )
    def list(self, request, *args, **kwargs):
        course = self.get_course()
        if not (self.is_course_instructor(course) or self.is_student_registered(course)):
            return Response(
                {"detail": "Access denied."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().list(request, *args, **kwargs)

class AssignmentDetailView(CourseAccessMixin, generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating and deleting assignments
    """
    serializer_class =CourseAssignmentCreateSerializer
    lookup_url_kwarg = 'assignment_slug'
    lookup_field = 'slug'
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsInstructor | IsStudent]

    @swagger_auto_schema(
        operation_description="Get a specific assignment",
        responses={
            200: CourseAssignmentCreateSerializer(),
            404: "Assignment not found"
        }
    )
    def get_object(self):
        course = self.get_course()
        return get_object_or_404(
            Assignment,
            course=course,
            slug=self.kwargs['assignment_slug']
        )

    def check_course_access(self):
        course = self.get_course()
        if not (self.is_course_instructor(course) or self.is_student_registered(course)):
            return Response(
                {"detail": "Access denied."},
                status=status.HTTP_403_FORBIDDEN
            )
        return None

    @swagger_auto_schema(
        operation_description="Retrieve an assignment",
        responses={
            200: CourseAssignmentCreateSerializer(),
            403: "Access denied",
            404: "Not found"
        }
    )
    def retrieve(self, request, *args, **kwargs):
        access_response = self.check_course_access()
        if access_response:
            return access_response
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an assignment",
        request_body=CourseAssignmentCreateSerializer,
        responses={
            200: CourseAssignmentCreateSerializer(),
            403: "Only instructor can update assignments",
            404: "Not found"
        }
    )
    def update(self, request, *args, **kwargs):
        course = self.get_course()
        if not self.is_course_instructor(course):
            return Response(
                {"detail": "Only instructor can update assignments."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an assignment",
        responses={
            204: "No content",
            403: "Only instructor can delete assignments",
            404: "Not found"
        }
    )
    def destroy(self, request, *args, **kwargs):
        course = self.get_course()
        if not self.is_course_instructor(course):
            return Response(
                {"detail": "Only instructor can delete assignments."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
class AssignmentSolutionView(CourseAccessMixin, generics.GenericAPIView):
    """
    API endpoint for managing assignment solutions
    """
    serializer_class = AssignmentSolutionSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsInstructor | IsStudent]

    def get_assignment(self):
        course = self.get_course()
        return get_object_or_404(
            Assignment,
            course=course,
            slug=self.kwargs['assignment_slug']
        )

    def get_student_solution(self):
        return Solution.objects.filter(
            assignment=self.get_assignment(),
            student=self.request.user.profile
        ).first()

    @swagger_auto_schema(
        operation_description="Submit a solution for an assignment",
        request_body=AssignmentSolutionSerializer,
        responses={
            201: AssignmentSolutionSerializer(),
            400: "Invalid request or solution already exists",
            403: "Permission denied"
        }
    )
    @ratelimit(key='ip', rate='5/m', block=True)
    def post(self, request, *args, **kwargs):
        course = self.get_course()
        assignment = self.get_assignment()

        if not self.is_student_registered(course):
            return Response(
                {"detail": "Only registered students can submit solutions."},
                status=status.HTTP_403_FORBIDDEN
            )

        if assignment.due_date < timezone.now().date():
            return Response(
                {"detail": "Assignment due date has passed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if self.get_student_solution():
            return Response(
                {"detail": "Solution already submitted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            assignment=assignment,
            student=request.user.profile
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @swagger_auto_schema(
    #     operation_description="Get solutions for an assignment",
    #     responses={
    #         200: openapi.Response(
    #             description="Success",
    #             schema=openapi.Schema(
    #                 type=openapi.TYPE_OBJECT,
    #                 oneOf=[
    #                     AssignmentSolutionSerializer,
    #                     StudentSolutionListSerializer
    #                 ]
    #             )
    #         ),
    #         403: "Access denied",
    #         404: "Solution not found"
    #     }
    # )
    def get(self, request, *args, **kwargs):
        course = self.get_course()
        assignment = self.get_assignment()

        if self.is_student_registered(course):
            solution = self.get_student_solution()
            if not solution:
                return Response(
                    {"detail": "No solution submitted."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response(
                self.get_serializer(solution).data,
                status=status.HTTP_200_OK
            )

        if self.is_course_instructor(course):
            solutions = Solution.objects.filter(assignment=assignment)
            return Response(
                StudentSolutionListSerializer(solutions, many=True).data,
                status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "Access denied."},
            status=status.HTTP_403_FORBIDDEN
        )

    @swagger_auto_schema(
        operation_description="Update a solution",
        request_body=AssignmentSolutionUpdateSerializer,
        responses={
            200: AssignmentSolutionUpdateSerializer(),
            400: "Invalid request or due date passed",
            403: "Permission denied",
            404: "Solution not found"
        }
    )
    def put(self, request, *args, **kwargs):
        course = self.get_course()
        assignment = self.get_assignment()
        
        if not self.is_student_registered(course):
            return Response(
                {"detail": "Only students can update solutions."},
                status=status.HTTP_403_FORBIDDEN
            )

        solution = self.get_student_solution()
        if not solution:
            return Response(
                {"detail": "No solution found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if assignment.due_date < timezone.now().date():
            return Response(
                {"detail": "Assignment due date has passed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AssignmentSolutionUpdateSerializer(
            solution,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete a solution",
        responses={
            204: "No content",
            400: "Due date passed",
            403: "Permission denied",
            404: "Solution not found"
        }
    )
    @ratelimit(key='ip', rate='5/m', block=True)
    def delete(self, request, *args, **kwargs):
        course = self.get_course()
        assignment = self.get_assignment()

        if not self.is_student_registered(course):
            return Response(
                {"detail": "Only students can delete solutions."},
                status=status.HTTP_403_FORBIDDEN
            )

        if assignment.due_date < timezone.now().date():
            return Response(
                {"detail": "Assignment due date has passed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        solution = self.get_student_solution()
        if not solution:
            return Response(
                {"detail": "No solution found."},
                status=status.HTTP_404_NOT_FOUND
            )

        solution.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AssignmentGradeListView(CourseAccessMixin, generics.ListCreateAPIView):
    """
    API endpoint for listing and creating assignment grades
    """
    serializer_class = AssignmentGradeListSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsInstructor]

    def get_assignment(self):
        course = self.get_course()
        return get_object_or_404(
            Assignment,
            course=course,
            slug=self.kwargs['assignment_slug']
        )

    @swagger_auto_schema(
        operation_description="Get list of grades for an assignment",
        responses={
            200: AssignmentGradeListSerializer(many=True),
            403: "Permission denied"
        }
    )
    def get_queryset(self):
        if not self.is_course_instructor(self.get_course()):
            return Grade.objects.none()
        return Grade.objects.filter(
            solution__assignment=self.get_assignment()
        )
