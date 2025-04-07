from rest_framework import serializers
from .models import Assignment , Grade
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




class SolutiontSerializer(serializers.ModelSerializer):
    grade = serializers.SerializerMethodField()
    class Meta:
        model = Grade
        fields = ( 'sloution', 'grade', )
        read_only_fields = ('grade', )
    def get_grade(self, obj):
        if obj.grade == -1:
            return "Not graded yet"
        return obj.grade



class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('assignment', 'student', 'sloution', 'grade', ) 
        read_only_fields = ('assignment', 'student','sloution' )