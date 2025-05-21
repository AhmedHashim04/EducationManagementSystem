from rest_framework import serializers
from .models import Course, CourseMaterial, CourseAssistant
from assignment.models import Assignment



class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['code', 'name','instructor_name','is_active','assistants', 'registration_start_at', 'registration_end_at']
    
    def get_assistants(self, obj):
        assistants = CourseAssistant.objects.filter(course=obj).values_list('assistant', flat=True)
        if assistants:
            return assistants
        return "No Assistants"
    def get_instructor_name(self, obj):
        if obj.instructor:
            return f"{obj.instructor.user.first_name} {obj.instructor.user.last_name}"
        return "Unknown"


class CourseDetailSerializer(serializers.ModelSerializer):
    registration_start_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", allow_null=True, required=False)
    registration_end_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", allow_null=True, required=False)

    def validate(self, data):
        if data['registration_start_at'] and data['registration_end_at']:
            if data['registration_start_at'] >= data['registration_end_at']:
                raise serializers.ValidationError({'registration_end_at': 'End date should be after start date'})
        return data

    class Meta:
        model = Course

        fields = [
            'name', 'code', 'description', 'created_at', #'manager_name',
            'updated_at', 'is_active', 'instructor_name', 'assignments', 'registration_start_at', 'registration_end_at'  # Fixed typo in 'assignments'
        ]
    def get_assistants(self, obj):
        assistants = CourseAssistant.objects.filter(course=obj).values_list('assistant', flat=True)
        if assistants:
            return assistants
        return "No Assistants"
    def get_assignments(self, obj):
        assignments =Assignment.objects.filter(course=obj).values_list('title', flat=True)
        if assignments:
            return assignments
        return "No Assignments"

    def get_instructor_name(self, obj):
        if obj.instructor:
            return f"{obj.instructor.user.first_name} {obj.instructor.user.last_name}"
        return "Unknown"


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