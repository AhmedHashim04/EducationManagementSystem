from rest_framework import serializers
from course.models import Course, CourseMaterial, CourseAssistant
from assignment.models import Assignment


# Utility Functions
def get_related_field_values(queryset, field_name, default="No Data"):
    """Utility function to fetch related field values."""
    values = queryset.values_list(field_name, flat=True)
    return values if values else default


class CourseListSerializer(serializers.ModelSerializer):
    """Serializer for listing courses."""
    instructor_name = serializers.SerializerMethodField()
    assistants = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['code', 'name', 'instructor_name', 'is_active', 'assistants', 'registration_start_at', 'registration_end_at']

    def get_assistants(self, obj):
        return get_related_field_values(
            CourseAssistant.objects.filter(course=obj), 'assistant__user__username', "No Assistants"
        )

    def get_instructor_name(self, obj):
        if obj.instructor:
            return f"{obj.instructor.user.first_name} {obj.instructor.user.last_name}"
        return "Unknown"


class CourseDetailSerializer(serializers.ModelSerializer):
    """Serializer for detailed course view."""
    materials = serializers.SerializerMethodField()
    assignments = serializers.SerializerMethodField()
    assistants = serializers.SerializerMethodField()
    instructor_name = serializers.SerializerMethodField()
    registration_start_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", allow_null=True, required=False)
    registration_end_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", allow_null=True, required=False)

    class Meta:
        model = Course
        fields = [
            'name', 'code', 'description', 'created_at', 'updated_at', 'is_active',
            'instructor_name', 'assistants', 'materials', 'assignments', 'registration_start_at', 'registration_end_at'
        ]

    def get_assistants(self, obj):
        return get_related_field_values(
            CourseAssistant.objects.filter(course=obj), 'assistant__user__username', "No Assistants"
        )

    def get_assignments(self, obj):
        return get_related_field_values(
            Assignment.objects.filter(course=obj), 'title', "No Assignments"
        )

    def get_instructor_name(self, obj):
        if obj.instructor:
            return f"{obj.instructor.user.first_name} {obj.instructor.user.last_name}"
        return "Unknown"

    def get_materials(self, obj):
        return get_related_field_values(
            CourseMaterial.objects.filter(course=obj), 'title', "No Materials"
        )


class CourseMaterialSerializer(serializers.ModelSerializer):
    """Serializer for course materials."""
    file_url = serializers.SerializerMethodField()
    video_url = serializers.URLField(read_only=True)
    pdf_file_url = serializers.SerializerMethodField()
    slides_file_url = serializers.SerializerMethodField()
    course_code = serializers.CharField(source='course.code', read_only=True)

    class Meta:
        model = CourseMaterial
        fields = (
            'id', 'course_code', 'title', 'description', 'file', 'file_url', 'video_url',
            'pdf_file', 'pdf_file_url', 'slides_file', 'slides_file_url', 'uploaded_at', 'updated_at', 'is_active'
        )
        read_only_fields = ('uploaded_at', 'updated_at', 'course_code')

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url') and request:
            return request.build_absolute_uri(obj.file.url)
        return None

    def get_pdf_file_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file and hasattr(obj.pdf_file, 'url') and request:
            return request.build_absolute_uri(obj.pdf_file.url)
        return None

    def get_slides_file_url(self, obj):
        request = self.context.get('request')
        if obj.slides_file and hasattr(obj.slides_file, 'url') and request:
            return request.build_absolute_uri(obj.slides_file.url)
        return None


class CourseAssistantSerializer(serializers.ModelSerializer):
    """Serializer for course assistants."""
    class Meta:
        model = CourseAssistant
        fields = ['assistant']