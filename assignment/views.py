from .models import Assignment, Solution , Grade
from rest_framework import generics 
from .serializer import CourseAssignmentsSerializer , ViewAssignmentsSerializer ,SolutionSerializer ,GradeSerializer ,UpdateSolutionSerializer , SudentsSolutionsSerializer
from account.permessions import  IsStudent, IsInstructor 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import timedelta
from django.utils import timezone
from course.models import Course  ,CourseRegistration
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from account.models import Profile

class CreatAssignment(generics.ListCreateAPIView):
    serializer_class = ViewAssignmentsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [ IsInstructor | IsStudent ]
    def is_student_registered(self, course):
        """Check if the current user is a student registered in the course."""
        return (
            self.request.user.profile.role == 'student' and
            CourseRegistration.objects.filter(student=self.request.user.profile, course=course).exists()
        )
    
    def is_the_real_instructor(self, course):
        """Check if the current user is the instructor of the course."""
        print(self.request.user.profile.role)
        return self.request.user.profile.role == 'instructor' and course.instructor == self.request.user.profile
        

    def get_course(self):
        course_code = self.kwargs['course_code']
        return get_object_or_404(Course, code=course_code)

    def get_queryset(self):
        course = self.get_course()
        return Assignment.objects.filter(course=course)

    def create(self, request, *args, **kwargs):
        course = self.get_course()
        print(self.is_the_real_instructor(course))
        if self.is_the_real_instructor(course):

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(course=course)

            return Response(serializer.data, status=201)
        
        return Response({"detail": "You do not have permission to create assignments for this course."}, status=403)

    def list(self, request, *args, **kwargs):
        course = self.get_course()

        if self.is_the_real_instructor(course) or self.is_student_registered(course):
            return super().list(request, *args, **kwargs)
        
        else:
            return Response({"detail": "You do not have permission to view assignments for this course."}, status=403)

class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseAssignmentsSerializer
    lookup_url_kwarg = 'assignment_id'
    authentication_classes = [JWTAuthentication]
    permission_classes = [ IsInstructor | IsStudent ]

    def is_student_registered(self, course):
        """Check if the current user is a student registered in the course."""
        return (
            self.request.user.profile.role == 'student' and
            CourseRegistration.objects.filter(student=self.request.user.profile, course=course).exists()
        )
    
    def is_the_real_instructor(self, course):
        """Check if the current user is the instructor of the course."""
        return self.request.user.profile.role == 'instructor' and course.instructor == self.request.user.profile
        

    def get_course(self):
        course_code = self.kwargs['course_code']
        return get_object_or_404(Course, code=course_code)

    def get_object(self):
        course_code = self.kwargs['course_code']
        assignment_id = self.kwargs['assignment_id']
        return get_object_or_404(Assignment, course__code=course_code, id=assignment_id)

    def retrieve(self, request, *args, **kwargs):
        course = self.get_course()
        if self.is_the_real_instructor(course) or self.is_student_registered(course):
            return super().retrieve(request, *args, **kwargs)

        return Response({"detail": "You do not have permission to view assignments for this course."}, status=403)

    def update(self, request, *args, **kwargs):
        course = self.get_course()
        if self.is_the_real_instructor(course):
            return super().update(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to update assignments for this course."}, status=403)

    def destroy(self, request, *args, **kwargs):
        course = self.get_course()
        if self.is_the_real_instructor(course):
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "You do not have permission to delete assignments for this course."}, status=403)

class SolveAssignment(generics.CreateAPIView,
                        generics.RetrieveAPIView,
                        generics.UpdateAPIView,
                        generics.DestroyAPIView):
        
    serializer_class = SolutionSerializer
    lookup_field = 'assignment_id'
    authentication_classes = [JWTAuthentication]
    permission_classes = [ IsInstructor | IsStudent ]
        

    def is_student_registered(self, course):
            """Check if the current user is a student registered in the course."""
            return (
                self.request.user.profile.role == 'student' and
                CourseRegistration.objects.filter(student=self.request.user.profile, course=course).exists()
            )
        
    def is_the_real_instructor(self, course):
            """Check if the current user is the instructor of the course."""
            return self.request.user.profile.role == 'instructor' and course.instructor == self.request.user.profile

    def get_course(self):
            course_code = self.kwargs['course_code']
            return get_object_or_404(Course, code=course_code)
        
    def get_assignment(self):
            assignment_id = self.kwargs['assignment_id']
            return get_object_or_404(Assignment, course=self.get_course(), id=assignment_id)
        
    def student_solution(self):
            student_id = self.request.user.profile
            return Solution.objects.filter(assignment=self.get_assignment(), student=student_id).first()

    def get_queryset(self):
            course = self.get_course()

            if self.is_student_registered(course):
                return Solution.objects.filter(student=self.request.user.profile).first()
            
            elif self.is_the_real_instructor(course):
                return Solution.objects.filter(assignment = self.get_assignment()).all()


    def create(self, request, *args, **kwargs):
            course = self.get_course()
            assignment = self.get_assignment()

            if self.is_student_registered(course):
                if assignment.due_date >= timezone.now().date():
                    if not self.student_solution():

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

            if self.is_student_registered(course):

                if self.student_solution():
                    assignment = self.get_assignment()
                    solution = self.student_solution()

                    assignment_serializer = ViewAssignmentsSerializer(assignment)
                    solution_serializer = SolutionSerializer(solution)

                    return Response({"assignment": assignment_serializer.data, "solution": solution_serializer.data}, status=404)
            
                else:
                    assignment = self.get_assignment()
                    serializer = ViewAssignmentsSerializer(assignment)
                    return Response({"assignment": serializer.data, "detail": "You have not submitted a solution for this assignment."}, status=404)
            
            elif self.is_the_real_instructor(course):
                assignment = self.get_assignment()
                solutions = Solution.objects.filter(assignment=assignment).all()

                assignment_serializer = ViewAssignmentsSerializer(assignment)
                solution_serializer = SudentsSolutionsSerializer(solutions, many=True)

                return Response({"assignment": assignment_serializer.data, "solutions": solution_serializer.data}, status=404)
                

            else:
                return Response({"detail": "You do not have permission to view solutions for this course."}, status=403)
            
    def update(self, request, *args, **kwargs):
            course = self.get_course()
            assignment = self.get_assignment()

            if self.is_student_registered(course):
                solution = self.student_solution()
                if not solution:
                    return Response({"detail": "You have not submitted a solution for this assignment."}, status=404)
                
                if assignment.due_date >= timezone.now().date():
                    serializer = UpdateSolutionSerializer(solution, data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data, status=200)
                else:
                    return Response({"detail": "The assignment is already past its due date."}, status=400)
            return Response({"detail": "You do not have permission to update solutions for this course."}, status=403)

    def destroy(self, request, *args, **kwargs):
            course = self.get_course()
            assignment = self.get_assignment()

            if self.is_student_registered(course):
                solution = self.student_solution()
                if not solution:
                    return Response({"detail": "You have not submitted a solution for this assignment."}, status=404)
                
                if assignment.due_date >= timezone.now().date():
                    solution = self.student_solution()
                    if solution:
                        solution.delete()
                        return Response({"detail": "Your solution has been successfully deleted."}, status=200)
                    return Response({"detail": "You have not submitted a solution for this assignment."}, status=404)
                else:
                    return Response({"detail": "The assignment is already past its due date."}, status=400)
            return Response({"detail": "You do not have permission to delete solutions for this course."}, status=403)
        
class GradeListView(generics.ListCreateAPIView):
    serializer_class = GradeSerializer
    queryset = Grade.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsInstructor]
    def is_the_real_instructor(self, course):
        """Check if the current user is the instructor of the course."""
        return self.request.user.profile.role == 'instructor' and course.instructor == self.request.user.profile
    
    def get_course(self):
        course_code = self.kwargs['course_code']
        return get_object_or_404(Course, code=course_code)
        
    def get_assignment(self):
        assignment_id = self.kwargs['assignment_id']
        return get_object_or_404(Assignment, course=self.get_course(), id=assignment_id)
    
    def get_queryset(self):
        course = self.get_course()
        assignment = self.get_assignment()
        if self.is_the_real_instructor(course):
            return Grade.objects.filter(solution__assignment=assignment)
        return super().get_queryset()
    


    # def list(self, request, *args, **kwargs):
    #     course = self.get_assignment().course

    #     if self.is_the_real_instructor(course):
    #         solutions = Solution.objects.filter(assignment=self.get_assignment())
    #         serializer = SolutionSerializer(solutions, many=True)
    #         return Response(serializer.data, status=200)
        
    #     return Response({"detail": "You do not have permission to view grades for this course."}, status=403)
    
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)