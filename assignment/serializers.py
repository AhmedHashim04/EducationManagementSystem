from rest_framework import serializers
from .models import Assignment , Solution ,Grade
from course.models import Course
from django.utils.timezone import now
from django.shortcuts import get_object_or_404

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('slug','title', 'description', 'due_date')

class CourseAssignmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating assignments within a course"""
    class Meta:
        model = Assignment
        fields = ('slug', 'title', 'description', 'due_date')
        read_only_fields = ('slug',)

    def create(self, validated_data):
        course = validated_data.pop('course', None)
        print(course)
        if course is None:
            raise serializers.ValidationError("Course is required to create an assignment")
        
        assignment = Assignment.objects.create(course=course, **validated_data)
        return assignment


class AssignmentSolutionSerializer(serializers.ModelSerializer):
    """Serializer for creating and retrieving individual assignment solutions"""
    student = serializers.StringRelatedField(read_only=True)
    assignment = serializers.StringRelatedField(read_only=True)
    submitted_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Solution
        fields = ('id', 'student', 'assignment', 'content', 'submitted_at', 'file_attachment')
        read_only_fields = ('id', 'student', 'assignment', 'submitted_at')

class AssignmentSolutionUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing assignment solutions"""
    class Meta:
        model = Solution
        fields = ('content', 'file_attachment')

class StudentSolutionListSerializer(serializers.ModelSerializer):
    """Serializer for listing all solutions submitted by students"""
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = Solution
        fields = ('id', 'student_name', 'assignment_title', 'content', 
                'submitted_at', 'file_attachment')

class AssignmentGradeListSerializer(serializers.ModelSerializer):
    """Serializer for listing all grades for assignments"""
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = Grade
        fields = ('id', 'student_name', 'assignment_title', 'score', 
                'feedback', 'graded_at')

class StudentGradeDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed view of a student's grade"""
    solution_content = serializers.CharField(source='solution.content', read_only=True)
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    
    class Meta:
        model = Grade
        fields = ('id', 'score', 'feedback', 'graded_at', 'solution_content',
                'assignment_title')
        read_only_fields = ('id', 'graded_at', 'solution_content', 'assignment_title')

