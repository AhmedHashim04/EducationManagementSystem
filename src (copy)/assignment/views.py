from django.shortcuts import render
from .models import Assignment, Grade
from rest_framework import generics 
from .serializer import CourseAssignmentsSerializer , ViewAssignmentsSerializer ,SolutiontSerializer ,GradeSerializer
from datetime import timedelta
from django.utils import timezone
from course.models import Course  ,CourseRegistration
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class CreateAssignment(generics.ListCreateAPIView):
    serializer_class = ViewAssignmentsSerializer

    def get_course(self):
        course_code = self.kwargs['course_code']
        return get_object_or_404(Course, code=course_code)

    def get_queryset(self):
        course = self.get_course()
        return Assignment.objects.filter(course=course)

    def create(self, request, *args, **kwargs):
        course = self.get_course()

        if request.user.profile == 'instructor' and course.instructor == request.user.profile:
            return super().create(request, *args, **kwargs)
        else:
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
        """
        دالة مساعدة للحصول على الكورس بناءً على `course_code`.
        """
        course_code = self.kwargs['course_code']
        return get_object_or_404(Course, code=course_code)

    def get_object(self):
        """
        دالة للحصول على الواجب بناءً على `course_code` و `assignment_id`.
        """
        course_code = self.kwargs['course_code']
        assignment_id = self.kwargs['assignment_id']
        return get_object_or_404(Assignment, course__code=course_code, id=assignment_id)

    def check_permissions(self, course):
        """
        دالة مساعدة للتحقق من صلاحيات المستخدم (student or instructor).
        """
        if self.request.user.profile.role == 'instructor' and course.instructor == self.request.user.profile:
            return 'instructor'
        elif self.request.user.profile.role == 'student':
            student_id = self.request.user.profile.id
            return 'student'
            # return CourseRegistration.objects.filter(student_id=student_id, course_id=course).exists()
        return False


    def retrieve(self, request, *args, **kwargs):
        course = self.get_course()
        if self.check_permissions(course):
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
    

class SolveAssignment(generics.CreateAPIView,
                      generics.UpdateAPIView,
                      generics.DestroyAPIView):
    serializer_class = SolutiontSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'assignment_id'

    def get_course(self):
        course_code = self.kwargs['course_code']
        return get_object_or_404(Course, code=course_code)

    def get_queryset(self):
        slug = self.kwargs['assignment_id']
        course_code = self.kwargs['course_code']
        return Assignment.objects.filter(course__code=course_code, id=slug)

    def check_permissions_and_due_date(self, assignment):

        """
        دالة مساعدة للتحقق من الأذونات وتاريخ الاستحقاق.
        """
        course = self.get_course()
        if self.request.user.profile == 'student' and Course.objects.filter(code=course.code, registrations__student_id=self.request.user.profile).exists():
            if assignment.due_date > timezone.now() + timedelta(days=1):
                return True
            else:
                return Response({"detail": "You cannot submit/update/delete an assignment after the due date."}, status=403)
        return Response({"detail": "You do not have permission to access assignments for this course."}, status=403)

    def create(self, request, *args, **kwargs):
        assignment = self.get_object()
        permission_check = self.check_permissions_and_due_date(assignment)
        if permission_check is True:
            return super().create(request, *args, **kwargs)
        return permission_check

    def update(self, request, *args, **kwargs):
        assignment = self.get_object()
        permission_check = self.check_permissions_and_due_date(assignment)
        if permission_check is True:
            return super().update(request, *args, **kwargs)
        return permission_check

    def destroy(self, request, *args, **kwargs):
        assignment = self.get_object()
        permission_check = self.check_permissions_and_due_date(assignment)
        if permission_check is True:
            return super().destroy(request, *args, **kwargs)
        return permission_check

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