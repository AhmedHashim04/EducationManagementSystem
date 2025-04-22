from rest_framework import serializers
from .models import Course
from assignment.models import Assignment

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'name']


class CourseDetailsSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField()
    instructor_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    assignments = serializers.SerializerMethodField()

    class Meta:
        model = Course

        fields = [
            'name', 'code', 'description', 'credit', 'created_at', 'manager_name',
            'updated_at', 'is_active', 'instructor_name', 'assignments'  # Fixed typo in 'assignments'
        ]
    def get_assignments(self, obj):
        assignments =Assignment.objects.filter(course=obj).values_list('title', flat=True)
        if assignments:
            return assignments
        return "No Assignments"

    def get_instructor_name(self, obj):
        if obj.instructor:
            return f"{obj.instructor.first_name} {obj.instructor.last_name}"
        return "Unknown"




        

#     def get_assignments(self, obj):
#         """
#         Get list of assignment titles for the course.
#         Returns list of titles or empty list if no assignments exist.
#         """
#         assignments = Assignment.objects.filter(course=obj).values_list('title', flat=True)
#         return list(assignments) or []  # Return empty list instead of string for consistency

#     def get_instructor_name(self, obj):
#         """
#         Get full name of course instructor.
#         Returns instructor's full name or 'Unknown' if no instructor assigned.
#         """
#         if not obj.instructor:
#             return "Unknown"
#         return f"{obj.instructor.first_name} {obj.instructor.last_name}".strip()

#     def get_manager_name(self, obj):
#         """
#         Get full name of course manager.
#         Returns manager's full name or 'Unknown' if no manager assigned.
#         """
#         if not obj.manager:
#             return "Unknown"
#         return f"{obj.manager.first_name} {obj.manager.last_name}".strip()
