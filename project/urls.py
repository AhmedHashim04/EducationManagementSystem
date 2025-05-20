
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="EducationManagementSystem API",
      default_version='v1',
      description="Documentation for all Sysyem API endpoints",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ahmedha4im7@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [

   path('admin/', admin.site.urls),
   path('account/', include('account.urls', namespace='account')),
   path('courses/', include('course.urls', namespace='course')),
   path('courses/me/', include('assignment.urls', namespace='assignment')),
   path('chat/', include('chat.urls', namespace='chat')),  
   path('api/', include('rest_framework.urls', namespace='rest_framework')),

   path('swagger<format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]





