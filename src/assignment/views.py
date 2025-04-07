from django.shortcuts import render
from .models import Assignment, Grade
from rest_framework import generics 
from .serializer import CourseAssignmentsSerializer , ViewAssignmentsSerializer ,SolutiontSerializer ,GradeSerializer
from datetime import timedelta
from django.utils import timezone
from course.models import Course  ,CourseRegistration
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class CreatAssignment(generics.ListCreateAPIView):
    serializer_class = ViewAssignmentsSerializer

    def get_course(self):
        course_code = self.kwargs['course_code']
        return get_object_or_404(Course, code=course_code)

    def get_queryset(self):
        course = self.get_course()
        return Assignment.objects.filter(course=course)

    def create(self, request, *args, **kwargs):
        course = self.get_course()

        if request.user.profile.role == 'instructor' and course.instructor == request.user.profile:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(course=course)
            return Response(serializer.data, status=201)
        
        # fallback response
        return Response({"detail": "You do not have permission to create assignments for this course."}, status=403)

    def list(self, request, *args, **kwargs):
        course = self.get_course()

        if request.user.profile.role == 'instructor' and course.instructor == request.user.profile:
            return super().list(request, *args, **kwargs)
        elif request.user.profile.role == 'student' and Course.objects.filter(code=course.code, registrations__student_id=request.user.profile).exists():
            return super().list(request, *args, **kwargs)
        else:
            return Response({"detail": "You do not have permission to view assignments for this course."}, status=403)


class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseAssignmentsSerializer
    lookup_url_kwarg = 'assignment_id'

    def get_course(self):
        course_code = self.kwargs['course_code']
        return get_object_or_404(Course, code=course_code)

    def get_object(self):
        course_code = self.kwargs['course_code']
        assignment_id = self.kwargs['assignment_id']
        return get_object_or_404(Assignment, course__code=course_code, id=assignment_id)

    def check_permissions(self, course):
        """
        دالة مساعدة للتحقق من صلاحيات المستخدم (student or instructor).
        """
        if self.request.user.profile.role == 'instructor' and self.get_course().instructor == self.request.user.profile:
            return 'instructor'
         
        elif self.request.user.profile.role == 'student':
            student_id = self.request.user.profile.id
            return 'student'
            # return CourseRegistration.objects.filter(student_id=student_id, course_id=course).exists()
        return False


    def retrieve(self, request, *args, **kwargs):
        course = self.get_course()
        if self.check_permissions(course) == 'instructor':
            return super().retrieve(request, *args, **kwargs)
        elif self.check_permissions(course) == 'student':
            return super().retrieve(request, *args, **kwargs)

        return Response({"detail": "You do not have permission to view assignments for this course."}, status=403)

    def update(self, request, *args, **kwargs):
        course = self.get_course()
        if self.check_permissions(course) == 'instructor':
            return super().update(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to update assignments for this course."}, status=403)

    def destroy(self, request, *args, **kwargs):
        course = self.get_course()
        if self.check_permissions(course) == 'instructor':
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to delete assignments for this course."}, status=403)
# Student Solve, Retrieve, Update, and Delete their solution

class SolveAssignment(generics.CreateAPIView,
                          generics.RetrieveAPIView,
                          generics.UpdateAPIView,
                          generics.DestroyAPIView):
        
        queryset = Grade.objects.all()
        serializer_class = SolutiontSerializer
        lookup_field = 'assignment_id'
        
        def get_course(self):
            course_code = self.kwargs['course_code']
            return get_object_or_404(Course, code=course_code)
        
        def get_assignment(self):
            assignment_id = self.kwargs['assignment_id']
            return get_object_or_404(Assignment, course=self.get_course(), id=assignment_id)
        
        def student_solution(self):
            student_id = self.request.user.profile.id
            return Grade.objects.filter(assignment=self.get_assignment(), student_id=student_id)

        def create(self, request, *args, **kwargs):
            course = self.get_course()
            assignment = self.get_assignment()

            if request.user.profile.role == 'student' and CourseRegistration.objects.filter(student_id=request.user.profile, course_id=course).exists():
                if assignment.due_date >= timezone.now().date():
                    if not self.student_solution().exists():
                        serializer = self.get_serializer(data=request.data)
                        serializer.is_valid(raise_exception=True)
                        serializer.save(assignment=assignment, student=request.user.profile)
                        return Response(serializer.data, status=201)
                    else:
                        return Response({"detail": "You have already submitted a solution for this assignment."}, status=400)
                else:
                        return Response({"detail": "The assignment is already past its due date."}, status=400)
            return Response({"detail": "You do not have permission to submit solutions for this course."}, status=403)

        def retrieve(self, request, *args, **kwargs):
            course = self.get_course()
            if request.user.profile.role == 'student' and CourseRegistration.objects.filter(student_id=request.user.profile, course_id=course).exists():
                if self.student_solution().exists():
                     assignment = self.get_assignment()
                     solution = self.student_solution().first()
                     assignment_serializer = ViewAssignmentsSerializer(assignment)
                     solution_serializer = SolutiontSerializer(solution)

                     return Response({"assignment": assignment_serializer.data, "solution": solution_serializer.data}, status=404)
            
            # elif request.user.profile.role == 'instructor' and course.instructor == request.user.profile:
                else:
                     assignment = self.get_assignment()
                     serializer = ViewAssignmentsSerializer(assignment)
                     return Response({"assignment": serializer.data, "detail": "You have not submitted a solution for this assignment."}, status=404)
            
            #     return super().retrieve(request, *args, **kwargs)
            else:
                return Response({"detail": "You do not have permission to view solutions for this course."}, status=403)
            
        def update(self, request, *args, **kwargs):
            course = self.get_course()
            assignment = self.get_assignment()

            if request.user.profile.role == 'student' and CourseRegistration.objects.filter(student_id=request.user.profile, course_id=course).exists():
                if assignment.due_date >= timezone.now().date():
                     return super().update(request, *args, **kwargs)
                else:
                    return Response({"detail": "The assignment is already past its due date."}, status=400)
            return Response({"detail": "You do not have permission to update solutions for this course."}, status=403)

        def destroy(self, request, *args, **kwargs):
            course = self.get_course()
            assignment = self.get_assignment()

            if request.user.profile.role == 'student' and CourseRegistration.objects.filter(student_id=request.user.profile, course_id=course).exists():
                if assignment.due_date >= timezone.now().date():
                    return super().destroy(request, *args, **kwargs)
                else:
                    return Response({"detail": "The assignment is already past its due date."}, status=400)
            return Response({"detail": "You do not have permission to delete solutions for this course."}, status=403)

class GradeAssignment(generics.UpdateAPIView):
    serializer_class = GradeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'assignment_id'

    def get_course(self):
        course_code = self.kwargs['course_code']
        return get_object_or_404(Course, code=course_code)

    def get_queryset(self):
        slug = self.kwargs['assignment_id']
        course_code = self.kwargs['course_code']
        return Assignment.objects.filter(course__code=course_code, id=slug)
    
    def update(self, request, *args, **kwargs):
        course = self.get_course()
        assignment = self.get_object()

        if request.user.profile == 'instructor' and course.instructor == request.user.profile:
            return super().update(request, *args, **kwargs)
        else:
            return Response({"detail": "You do not have permission to grade assignments for this course."}, status=403)