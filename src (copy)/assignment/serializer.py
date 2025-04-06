from rest_framework import serializers
from .models import Assignment , Grade

from django.utils.timezone import now

class CourseAssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('title', 'description', 'course', 'due_date', )
        read_only_fields = ('course','id')


class ViewAssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('title', 'description', 'course', 'due_date', 'id')
        read_only_fields = ('title', 'description', 'course', 'due_date', 'id')


class SolutiontSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('assignment', 'student', 'sloution', 'grade', )
        read_only_fields = ('assignment', 'student', 'grade', )



class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('assignment', 'student', 'sloution', 'grade', ) 