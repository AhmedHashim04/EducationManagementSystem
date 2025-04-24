from rest_framework import serializers
from .models import Course, CourseMaterial
from assignment.models import Assignment

class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'name']


class CourseDetailSerializer(serializers.ModelSerializer):
    # manager_name = serializers.SerializerMethodField()
    instructor_name = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    assignments = serializers.SerializerMethodField()

    class Meta:
        model = Course

        fields = [
            'name', 'code', 'description', 'credit', 'created_at', #'manager_name',
            'updated_at', 'is_active', 'instructor_name', 'assignments'  # Fixed typo in 'assignments'
        ]
    def get_assignments(self, obj):
        assignments =Assignment.objects.filter(course=obj).values_list('title', flat=True)
        if assignments:
            return assignments
        return "No Assignments"

    def get_instructor_name(self, obj):
        if obj.instructor:
            return f"{obj.instructor.user.first_name} {obj.instructor.user.last_name}"
        return "Unknown"

    # def get_manager_name(self, obj):
    #     """
    #     Get full name of course manager.
    #     Returns manager's full name or 'Unknown' if no manager assigned.
    #     """
    #     if not obj.manager:
    #         return "Unknown"
    #     return f"{obj.manager.user.first_name} {obj.manager.user.last_name}".strip()



class CourseMaterialSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    course_code = serializers.CharField(source='course.code', read_only=True)

    class Meta:
        model = CourseMaterial
        fields = (
            'id', 
            'course_code',
            'title', 
            'description', 
            'file',
            'file_url',
            'uploaded_at',
            'updated_at',
            'is_active'
        )
        read_only_fields = ('uploaded_at', 'updated_at', 'course_code')

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url') and request:
            return request.build_absolute_uri(obj.file.url)
        return None