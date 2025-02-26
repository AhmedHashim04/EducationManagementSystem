from django.contrib import admin

# Register your models here.
from .models import Assignment , Grade

admin.site.register(Assignment)
admin.site.register(Grade)