from rest_framework import serializers
from .models import Assignment , Grade

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ('title', 'description', 'course', 'due_date', )



# class GradeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Grade
#         fields = ('assignment', 'student', 'sloution', 'grade', ) 