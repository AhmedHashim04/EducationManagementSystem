from rest_framework import serializers
from .models import Assignment , Solution ,Grade
from course.models import Course
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

class CourseAssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('title', 'description', 'course', 'due_date', )
        read_only_fields = ('course','id')

class ViewAssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('title', 'description', 'course', 'due_date')
        read_only_fields = ('course', 'id')




class SolutionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = Solution
        fields = ('id', 'assignment', 'assignment_title', 'student', 'student_name', 'sloution')
        read_only_fields = ('id', 'assignment_title', 'student_name')

class UpdateSolutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solution
        fields = ('sloution',)
        read_only_fields = ('id', 'assignment', 'assignment_title', 'student', 'student_name', )


class SudentsSolutionsSerializer(serializers.ModelSerializer):
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)

    class Meta:
        model = Solution
        fields = ('id', 'assignment', 'assignment_title', 'student', 'sloution')
        read_only_fields = ('id', 'assignment_title', 'student_name')



class GradeSerializer(serializers.ModelSerializer):
    solution_details = serializers.SerializerMethodField()
    graded_by = serializers.CharField(source='graded_by.get_full_name', read_only=True)

    class Meta:
        model = Grade
        fields = ('id', 'solution', 'solution_details', 'grade', 'comment', 'graded_by', 'created_at', 'updated_at')
        read_only_fields = ('id', 'solution', 'solution_details', 'graded_by', 'created_at', 'updated_at')

    def get_solution_details(self, obj):
        return {
            "assignment_title": obj.solution.assignment.title,
            "student_name": obj.solution.student.user.get_full_name,
            "submission_date": obj.solution.created_at
        }

class GradeStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ('id', 'solution', 'grade', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id','solution', 'created_at', 'updated_at')
